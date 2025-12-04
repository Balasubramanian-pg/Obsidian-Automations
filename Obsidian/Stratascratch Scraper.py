"""
StrataScratch SQL Questions Scraper
Scrapes all PostgreSQL analytical questions from StrataScratch and saves to markdown files.

ENHANCED VERSION with robust error handling and edge case management.
"""

import requests
from bs4 import BeautifulSoup
import time
import re
import os
from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class StrataScratchScraper:
    def __init__(self, output_dir: str = "stratascratch_questions"):
        self.base_url = "https://platform.stratascratch.com"
        self.questions_url = f"{self.base_url}/coding?code_type=1"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        self.log = []
        self.scraped_count = 0
        self.failed_count = 0
        self.max_retries = 3
        self.retry_delay = 5
        
        logging.info(f"Scraper initialized. Output directory: {self.output_dir.absolute()}")
    
    def slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug with improved handling."""
        if not text or text == "Unknown":
            return f"unknown-question-{int(time.time())}"
        
        # Remove any content in parentheses or brackets
        text = re.sub(r'[\(\[].*?[\)\]]', '', text)
        
        # Convert to lowercase and replace problematic characters
        text = text.lower()
        text = re.sub(r'[^a-z0-9]+', '-', text)
        text = re.sub(r'-+', '-', text)
        text = text.strip('-')
        
        # Ensure filename isn't too long (max 200 chars)
        if len(text) > 200:
            text = text[:200].rstrip('-')
        
        # If empty after processing, generate a fallback
        if not text:
            text = f"question-{int(time.time())}"
        
        return text
    
    def extract_question_links(self, page_num: int = 1) -> List[str]:
        """Extract all question links from a page with retry logic."""
        url = f"{self.questions_url}&page={page_num}"
        logging.info(f"Fetching page {page_num}: {url}")
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all question links
                question_links = []
                
                # Multiple selector strategies in case page structure varies
                # Strategy 1: Primary selector
                links = soup.find_all('a', class_='group contents')
                
                # Strategy 2: Fallback - find any link with /coding/ in href
                if not links:
                    all_links = soup.find_all('a', href=True)
                    links = [l for l in all_links if '/coding/' in l.get('href', '')]
                
                for link in links:
                    href = link.get('href')
                    if href and '/coding/' in href and '?code_type' in href:
                        # Handle both absolute and relative URLs
                        if href.startswith('http'):
                            full_url = href
                        else:
                            full_url = f"{self.base_url}{href}"
                        
                        # Deduplicate
                        if full_url not in question_links:
                            question_links.append(full_url)
                
                if question_links:
                    logging.info(f"Found {len(question_links)} questions on page {page_num}")
                    return question_links
                else:
                    logging.warning(f"No questions found on page {page_num}")
                    return []
                
            except requests.exceptions.Timeout:
                logging.warning(f"Timeout on page {page_num}, attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    
            except requests.exceptions.RequestException as e:
                logging.error(f"Request error on page {page_num}, attempt {attempt + 1}/{self.max_retries}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    
            except Exception as e:
                logging.error(f"Unexpected error on page {page_num}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        logging.error(f"Failed to fetch page {page_num} after {self.max_retries} attempts")
        return []
    
    def extract_text_from_pills(self, container, heading: str) -> List[str]:
        """Extract text from pill elements under a specific heading with error handling."""
        items = []
        if not container:
            return items
            
        try:
            # Find the heading - try multiple approaches
            h3 = container.find('h3', string=heading)
            
            # If exact match fails, try case-insensitive
            if not h3:
                all_h3 = container.find_all('h3')
                for h in all_h3:
                    if h.get_text(strip=True).lower() == heading.lower():
                        h3 = h
                        break
            
            if h3:
                # Get the next sibling div with pills
                pills_container = h3.find_next_sibling('div')
                if pills_container:
                    pills = pills_container.find_all('div', class_='QuestionMetadata__pill')
                    items = [pill.get_text(strip=True) for pill in pills if pill.get_text(strip=True)]
        except Exception as e:
            logging.warning(f"Error extracting pills for '{heading}': {e}")
        
        return items
    
    def scrape_question_details(self, url: str) -> Optional[Dict]:
        """Scrape all details from a question page with comprehensive error handling."""
        logging.info(f"Scraping: {url}")
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract title with fallback
                title = "Unknown"
                title_elem = soup.find('h1', class_='QuestionMetadata__h1')
                if title_elem:
                    # Remove SVG/icon elements
                    for svg in title_elem.find_all('svg'):
                        svg.decompose()
                    title = title_elem.get_text(strip=True)
                
                # If title still not found, try alternative selectors
                if title == "Unknown":
                    title_elem = soup.find('h1')
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                
                # Extract ID with multiple strategies
                question_id = "Unknown"
                # Strategy 1: Direct regex match
                id_elem = soup.find('span', string=re.compile(r'ID\s*\d+'))
                if id_elem:
                    question_id = id_elem.get_text(strip=True)
                else:
                    # Strategy 2: Extract from URL
                    id_match = re.search(r'/coding/(\d+)-', url)
                    if id_match:
                        question_id = f"ID {id_match.group(1)}"
                
                # Extract difficulty with fallback
                difficulty = "Unknown"
                difficulty_elem = soup.find('span', class_=re.compile(r'QuestionDifficulty--'))
                if difficulty_elem:
                    # Remove SVG icons
                    for svg in difficulty_elem.find_all('svg'):
                        svg.decompose()
                    difficulty_text = difficulty_elem.get_text(strip=True)
                    # Extract just the difficulty word
                    for level in ['Easy', 'Medium', 'Hard']:
                        if level.lower() in difficulty_text.lower():
                            difficulty = level
                            break
                
                # Extract difficulty reason
                difficulty_reason = ""
                reason_elem = soup.find('span', class_='QuestionDifficulty__reason-text')
                if reason_elem:
                    difficulty_reason = reason_elem.get_text(strip=True)
                
                # Extract last updated date
                last_updated = "Unknown"
                date_elem = soup.find('p', class_='QuestionMetadata__date')
                if date_elem:
                    last_updated = date_elem.get_text(strip=True)
                
                # Extract question description with fallback
                question_text = "No description available"
                question_elem = soup.find('div', class_='QuestionMetadata__question')
                if question_elem:
                    # Get all text including paragraphs
                    paragraphs = question_elem.find_all(['p', 'div'])
                    if paragraphs:
                        question_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                    else:
                        question_text = question_elem.get_text(strip=True)
                
                # Extract metadata container
                metadata_container = soup.find('div', class_='pb-4 pt-0')
                
                companies = []
                job_positions = []
                topic_family = []
                topic_functions = []
                
                if metadata_container:
                    companies = self.extract_text_from_pills(metadata_container, 'Companies')
                    job_positions = self.extract_text_from_pills(metadata_container, 'Job Positions')
                    topic_family = self.extract_text_from_pills(metadata_container, 'Topic Family')
                    topic_functions = self.extract_text_from_pills(metadata_container, 'Topic Functions')
                
                # Extract upvotes with fallback
                upvotes = "0"
                metadata_div = soup.find('div', class_='QuestionMetadata__metadata')
                if metadata_div:
                    vote_span = metadata_div.find('span', class_='py-2')
                    if vote_span:
                        upvotes_text = vote_span.get_text(strip=True)
                        if upvotes_text.isdigit():
                            upvotes = upvotes_text
                
                # Validate critical fields
                if title == "Unknown" and question_id == "Unknown":
                    logging.warning(f"Could not extract critical data from {url}")
                    # Try one more time with different approach
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                        continue
                
                data = {
                    'title': title,
                    'id': question_id,
                    'difficulty': difficulty,
                    'difficulty_reason': difficulty_reason,
                    'last_updated': last_updated,
                    'question': question_text,
                    'companies': companies,
                    'job_positions': job_positions,
                    'topic_family': topic_family,
                    'topic_functions': topic_functions,
                    'upvotes': upvotes,
                    'url': url
                }
                
                logging.info(f"Successfully scraped: {title}")
                return data
                
            except requests.exceptions.Timeout:
                logging.warning(f"Timeout scraping {url}, attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    
            except requests.exceptions.RequestException as e:
                logging.error(f"Request error scraping {url}, attempt {attempt + 1}/{self.max_retries}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    
            except Exception as e:
                logging.error(f"Unexpected error scraping {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        logging.error(f"Failed to scrape {url} after {self.max_retries} attempts")
        return None
    
    def create_markdown(self, data: Dict) -> str:
        """Generate markdown content from question data."""
        md = f"# {data['title']}\n\n"
        md += f"**ID:** {data['id']}  \n"
        md += f"**Difficulty:** {data['difficulty']}  \n"
        md += f"**Last Updated:** {data['last_updated']}  \n"
        md += f"**Source URL:** {data['url']}\n\n"
        md += "---\n\n"
        
        if data['difficulty_reason']:
            md += "## Difficulty Explanation\n"
            md += f"{data['difficulty_reason']}\n\n"
            md += "---\n\n"
        
        md += "## Question\n"
        md += f"{data['question']}\n\n"
        md += "---\n\n"
        
        if data['companies']:
            md += "## Companies\n"
            md += ", ".join(data['companies']) + "\n\n"
        
        if data['job_positions']:
            md += "## Job Positions\n"
            md += ", ".join(data['job_positions']) + "\n\n"
        
        if data['topic_family']:
            md += "## Topic Family\n"
            md += ", ".join(data['topic_family']) + "\n\n"
        
        if data['topic_functions']:
            md += "## Topic Functions\n"
            md += ", ".join(data['topic_functions']) + "\n\n"
        
        md += "---\n\n"
        md += f"**Upvotes:** {data['upvotes']}\n"
        
        return md
    
    def save_question(self, data: Dict) -> bool:
        """Save question data to markdown file with duplicate handling."""
        try:
            base_filename = self.slugify(data['title'])
            filename = f"{base_filename}.md"
            filepath = self.output_dir / filename
            
            # Handle duplicate filenames
            counter = 1
            while filepath.exists():
                # Check if it's actually the same question by comparing ID
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        existing_content = f.read()
                        if data['id'] in existing_content:
                            logging.info(f"Question already exists: {filename}")
                            return True
                except:
                    pass
                
                # If different question with same name, append counter
                filename = f"{base_filename}-{counter}.md"
                filepath = self.output_dir / filename
                counter += 1
            
            markdown_content = self.create_markdown(data)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logging.info(f"Saved: {filename}")
            self.scraped_count += 1
            return True
            
        except UnicodeEncodeError as e:
            logging.error(f"Unicode error saving {data['title']}: {e}")
            # Try with ASCII-safe filename
            try:
                safe_filename = f"question-{data['id'].replace('ID ', '')}.md"
                filepath = self.output_dir / safe_filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(self.create_markdown(data))
                logging.info(f"Saved with safe filename: {safe_filename}")
                self.scraped_count += 1
                return True
            except Exception as e2:
                logging.error(f"Failed to save with safe filename: {e2}")
                self.failed_count += 1
                return False
                
        except Exception as e:
            logging.error(f"Error saving {data['title']}: {e}")
            self.failed_count += 1
            return False
    
    def get_total_pages(self) -> int:
        """Determine total number of pages with retry logic."""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(self.questions_url, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find pagination buttons
                pagination_buttons = soup.find_all('button', class_='Pagination__button')
                page_numbers = []
                
                for button in pagination_buttons:
                    text = button.get_text(strip=True)
                    if text.isdigit():
                        page_numbers.append(int(text))
                
                if page_numbers:
                    total = max(page_numbers)
                    logging.info(f"Detected {total} total pages")
                    return total
                else:
                    logging.warning("Could not find pagination, defaulting to 1 page")
                    return 1
                    
            except Exception as e:
                logging.error(f"Error getting total pages, attempt {attempt + 1}/{self.max_retries}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        logging.warning("Failed to determine total pages, defaulting to 1")
        return 1
    
    def scrape_all_questions(self, max_pages: Optional[int] = None, resume_from: Optional[int] = None):
        """Main scraping function - scrapes all questions across all pages.
        
        Args:
            max_pages: Limit scraping to first N pages (for testing)
            resume_from: Resume scraping from question index (for recovery)
        """
        print("=" * 70)
        print("🚀 StrataScratch SQL Questions Scraper Started")
        print("=" * 70)
        
        start_time = time.time()
        
        # Determine total pages
        total_pages = self.get_total_pages()
        if max_pages:
            total_pages = min(total_pages, max_pages)
        
        logging.info(f"Total pages to scrape: {total_pages}")
        
        all_question_urls = []
        
        # Step 1: Collect all question URLs
        logging.info("=" * 70)
        logging.info("Step 1: Collecting all question URLs")
        logging.info("=" * 70)
        
        for page in range(1, total_pages + 1):
            question_links = self.extract_question_links(page)
            all_question_urls.extend(question_links)
            time.sleep(1.5)  # Rate limiting between page requests
        
        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in all_question_urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        all_question_urls = unique_urls
        
        logging.info(f"Total unique questions found: {len(all_question_urls)}")
        
        if not all_question_urls:
            logging.error("No questions found! Check if website structure has changed.")
            return
        
        # Step 2: Scrape each question
        logging.info("=" * 70)
        logging.info("Step 2: Scraping detailed question data")
        logging.info("=" * 70)
        
        start_index = resume_from if resume_from else 0
        
        for idx in range(start_index, len(all_question_urls)):
            url = all_question_urls[idx]
            logging.info(f"[{idx + 1}/{len(all_question_urls)}]")
            
            question_data = self.scrape_question_details(url)
            
            if question_data:
                success = self.save_question(question_data)
                self.log.append({
                    'index': idx,
                    'url': url,
                    'title': question_data['title'],
                    'id': question_data['id'],
                    'status': 'success' if success else 'failed_save',
                    'timestamp': datetime.now().isoformat()
                })
            else:
                self.failed_count += 1
                self.log.append({
                    'index': idx,
                    'url': url,
                    'title': 'Unknown',
                    'id': 'Unknown',
                    'status': 'failed_scrape',
                    'timestamp': datetime.now().isoformat()
                })
            
            # Save intermediate log every 10 questions
            if (idx + 1) % 10 == 0:
                self.save_log()
            
            # Rate limiting - be respectful to the server
            time.sleep(2)
        
        # Save final log
        self.save_log()
        
        # Summary
        elapsed_time = time.time() - start_time
        print("\n" + "=" * 70)
        print("✨ SCRAPING COMPLETE")
        print("=" * 70)
        print(f"✅ Successfully scraped: {self.scraped_count}")
        print(f"❌ Failed: {self.failed_count}")
        print(f"📊 Success rate: {(self.scraped_count/(self.scraped_count+self.failed_count)*100):.1f}%")
        print(f"⏱️  Time elapsed: {elapsed_time/60:.1f} minutes")
        print(f"📁 Files saved to: {self.output_dir.absolute()}")
        print("=" * 70)
        
        logging.info("Scraping completed successfully")
    
    def save_log(self):
        """Save scraping log to JSON file."""
        log_file = self.output_dir / "scraping_log.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({
                'total_scraped': self.scraped_count,
                'total_failed': self.failed_count,
                'timestamp': datetime.now().isoformat(),
                'details': self.log
            }, f, indent=2)
        print(f"\n📝 Log saved to: {log_file}")


# Usage
if __name__ == "__main__":
    scraper = StrataScratchScraper(output_dir="stratascratch_questions")
    
    # Scrape all questions (remove max_pages parameter to scrape everything)
    scraper.scrape_all_questions()
    
    # To test with just first 2 pages:
    # scraper.scrape_all_questions(max_pages=2)