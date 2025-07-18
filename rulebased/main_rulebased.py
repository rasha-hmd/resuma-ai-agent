import fitz  # PyMuPDF
import re
from collections import Counter
from pathlib import Path


class ResumeJobMatcher:
    def __init__(self):
        # Pre-compiled regex patterns for efficiency
        self.skill_patterns = re.compile(
            r'\b(?:python|java|javascript|react|angular|vue|node|sql|mysql|postgresql|'
            r'mongodb|aws|azure|gcp|docker|kubernetes|git|jenkins|ci/cd|agile|scrum|'
            r'machine learning|ai|data science|tensorflow|pytorch|pandas|numpy|'
            r'html|css|bootstrap|tailwind|django|flask|express|spring|hibernate|'
            r'restful|api|microservices|devops|linux|windows|macos)\b',
            re.IGNORECASE
        )

        self.role_patterns = re.compile(
            r'\b(?:manager|senior|lead|principal|architect|engineer|developer|'
            r'analyst|specialist|consultant|coordinator|director|designer|'
            r'administrator|intern|junior|associate)\b',
            re.IGNORECASE
        )

        self.industry_patterns = re.compile(
            r'\b(?:healthcare|finance|fintech|e-commerce|retail|education|'
            r'manufacturing|automotive|aerospace|telecommunications|media|'
            r'gaming|saas|startup|enterprise|consulting)\b',
            re.IGNORECASE
        )

        # Common stop words to filter out
        self.stop_words = {
            'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
            'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF with error handling"""
        try:
            doc = fitz.open(pdf_path)
            text_parts = []
            for page in doc:
                text_parts.append(page.get_text())
            doc.close()
            return ' '.join(text_parts)
        except Exception as e:
            raise Exception(f"Error reading PDF: {e}")

    def extract_keywords_optimized(self, text):
        """Extract keywords using rule-based approach with multiple categories"""
        text_lower = text.lower()

        # Extract different types of keywords
        skills = set(self.skill_patterns.findall(text_lower))
        roles = set(self.role_patterns.findall(text_lower))
        industries = set(self.industry_patterns.findall(text_lower))

        # Extract general keywords (nouns and proper nouns)
        # Split by common delimiters and filter
        words = re.findall(r'\b[a-zA-Z]{2,}\b', text_lower)
        general_keywords = {
            word for word in words
            if word not in self.stop_words
               and len(word) > 2
               and not word.isdigit()
        }

        # Remove duplicates across categories
        all_keywords = skills | roles | industries | general_keywords

        return {
            'skills': skills,
            'roles': roles,
            'industries': industries,
            'general': general_keywords - skills - roles - industries,
            'all': all_keywords
        }

    def compute_enhanced_match(self, resume_keywords, job_keywords):
        """Compute weighted matching score with category breakdown"""
        # Weights for different keyword categories
        weights = {
            'skills': 0.4,  # Technical skills are most important
            'roles': 0.2,  # Role-related keywords
            'industries': 0.2,  # Industry experience
            'general': 0.2  # General keywords
        }

        results = {}
        total_weighted_score = 0

        for category in ['skills', 'roles', 'industries', 'general']:
            resume_cat = resume_keywords[category]
            job_cat = job_keywords[category]

            if job_cat:
                matched = resume_cat & job_cat
                missing = job_cat - resume_cat
                score = (len(matched) / len(job_cat)) * 100
                weighted_score = score * weights[category]
                total_weighted_score += weighted_score

                results[category] = {
                    'score': score,
                    'weighted_score': weighted_score,
                    'matched': matched,
                    'missing': missing,
                    'total_job_keywords': len(job_cat)
                }
            else:
                results[category] = {
                    'score': 0,
                    'weighted_score': 0,
                    'matched': set(),
                    'missing': set(),
                    'total_job_keywords': 0
                }

        # Overall score
        overall_matched = resume_keywords['all'] & job_keywords['all']
        overall_missing = job_keywords['all'] - resume_keywords['all']
        overall_simple_score = (len(overall_matched) / len(job_keywords['all'])) * 100 if job_keywords['all'] else 0

        return {
            'weighted_score': total_weighted_score,
            'simple_score': overall_simple_score,
            'category_results': results,
            'overall_matched': overall_matched,
            'overall_missing': overall_missing
        }

    def get_keyword_frequency(self, text, keywords):
        """Get frequency of keywords in text for better matching"""
        text_lower = text.lower()
        freq = Counter()
        for keyword in keywords:
            count = len(re.findall(rf'\b{re.escape(keyword)}\b', text_lower))
            if count > 0:
                freq[keyword] = count
        return freq

    def analyze_match(self, resume_path, job_description_path):
        """Main analysis function with comprehensive results"""
        # Validate file paths
        if not Path(resume_path).exists():
            raise FileNotFoundError(f"Resume file not found: {resume_path}")
        if not Path(job_description_path).exists():
            raise FileNotFoundError(f"Job description file not found: {job_description_path}")

        # Extract text
        resume_text = self.extract_text_from_pdf(resume_path)
        with open(job_description_path, "r", encoding="utf-8") as f:
            job_description = f.read()

        # Extract keywords
        resume_keywords = self.extract_keywords_optimized(resume_text)
        job_keywords = self.extract_keywords_optimized(job_description)

        # Compute match
        match_results = self.compute_enhanced_match(resume_keywords, job_keywords)

        # Get keyword frequencies for better insights
        job_keyword_freq = self.get_keyword_frequency(job_description, job_keywords['all'])
        resume_keyword_freq = self.get_keyword_frequency(resume_text, resume_keywords['all'])

        return {
            'match_results': match_results,
            'job_keyword_freq': job_keyword_freq,
            'resume_keyword_freq': resume_keyword_freq,
            'resume_keywords': resume_keywords,
            'job_keywords': job_keywords
        }

    def print_results(self, analysis_results):
        """Print formatted results"""
        match_results = analysis_results['match_results']

        print("\n" + "=" * 60)
        print("📊 RESUME-JOB MATCHING ANALYSIS")
        print("=" * 60)

        print(f"\n🎯 OVERALL SCORES:")
        print(f"   Weighted Score: {match_results['weighted_score']:.1f}%")
        print(f"   Simple Score: {match_results['simple_score']:.1f}%")

        print(f"\n📋 CATEGORY BREAKDOWN:")
        for category, results in match_results['category_results'].items():
            if results['total_job_keywords'] > 0:
                print(f"\n   {category.upper()}:")
                print(f"      Score: {results['score']:.1f}% (Weight: {results['weighted_score']:.1f}%)")
                print(
                    f"      Matched ({len(results['matched'])}): {', '.join(sorted(results['matched'])) if results['matched'] else 'None'}")
                if results['missing']:
                    missing_sorted = sorted(results['missing'])[:10]  # Show top 10 missing
                    print(
                        f"      Missing ({len(results['missing'])}): {', '.join(missing_sorted)}{'...' if len(results['missing']) > 10 else ''}")

        print(f"\n✅ TOP MATCHED KEYWORDS:")
        top_matched = sorted(match_results['overall_matched'])[:15]
        print(f"   {', '.join(top_matched) if top_matched else 'None'}")

        # Recommendation
        if match_results['weighted_score'] >= 70:
            print(f"\n🎉 RECOMMENDATION: Strong match! This resume aligns well with the job requirements.")
        elif match_results['weighted_score'] >= 50:
            print(f"\n💡 RECOMMENDATION: Good potential. Consider highlighting missing key skills.")
        else:
            print(f"\n⚠️  RECOMMENDATION: Significant gaps. Focus on developing missing technical skills.")


def main():
    matcher = ResumeJobMatcher()

    try:
        resume_path = input("Enter path to resume PDF: ").strip()
        job_description_path = input("Enter path to job description text file: ").strip()

        print("\n🔍 Analyzing resume against job description...")

        analysis_results = matcher.analyze_match(resume_path, job_description_path)
        matcher.print_results(analysis_results)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your file paths and try again.")


if __name__ == "__main__":
    main()