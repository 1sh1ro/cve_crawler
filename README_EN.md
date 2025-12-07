# CVE Information Scraper 🔍

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![NVD API](https://img.shields.io/badge/NVD-API%202.0-orange.svg)](https://nvd.nist.gov/developers)

A CVE vulnerability information scraper based on the official NVD API, supporting search by date range and keywords to obtain complete CVE details.

## ✨ Features

- 🎯 **Precise Search**: Support keyword, date range, and CPE name filtering
- 📊 **Complete Information**: Get CVSS scores, CWE types, affected products, reference links, and more
- 🚀 **High Performance**: Support NVD API key for 10x speed boost
- 💾 **Multiple Export Formats**: Support JSON, CSV, and Markdown formats
- 🔄 **Auto Segmentation**: Automatically handle NVD API's 120-day limitation
- ⚡ **Rate Control**: Intelligently handle API rate limits to avoid blocking
- 🛡️ **Stable and Reliable**: Based on official API, accurate and compliant data

## 📋 Information Retrieved

Each CVE contains the following complete information:

- CVE ID
- Published date and last modified date
- Vulnerability status
- Complete vulnerability description
- CVSS v3/v2 score and severity
- CVSS vector string
- Exploitability score and impact score
- CWE vulnerability type classification
- Affected products and versions (CPE format)
- Official reference links

## 🚀 Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Basic Usage

```bash
# Scrape Linux kernel privilege escalation vulnerabilities from the last 5 years
python cve_scraper.py -k "linux kernel privilege escalation"

# Specify time range
python cve_scraper.py -k "apache" -s "2023-01-01 00:00" -e "2023-12-31 23:59"

# Scrape Windows vulnerabilities from the last 3 years
python cve_scraper.py -k "windows" -y 3
```

### Using API Key (Highly Recommended)

```bash
python cve_scraper.py -k "docker" -y 2 --api-key YOUR_API_KEY
```

## 🔑 Get NVD API Key

**Highly recommended to apply for a free API key to boost speed!**

| Mode | Rate Limit | Speed Comparison |
|------|-----------|------------------|
| Without API Key | 5 requests/30s | Baseline |
| With API Key | 50 requests/30s | **10x Faster** |

### Application Steps

1. Visit [NVD API Key Request Page](https://nvd.nist.gov/developers/request-an-api-key)
2. Fill in your email address
3. Check your email and click the confirmation link
4. Enter your email and UUID on the confirmation page
5. Get your API key

## 📖 Usage Guide

### Command Line Arguments

```
Required:
  -k, --keyword KEYWORD        Search keyword

Optional:
  -s, --start-date START       Start date, format: YYYY-MM-DD HH:MM
  -e, --end-date END           End date, format: YYYY-MM-DD HH:MM
  -y, --years YEARS            Recent N years (default: 5)
  --cpe CPE                    CPE name filter
  --api-key API_KEY            NVD API key
  -o, --output PREFIX          Output filename prefix (default: cve_results)
  --json-only                  Save JSON format only
  --csv-only                   Save CSV format only
  --md-only                    Save Markdown format only
```

### Usage Examples

#### 1. Linux Kernel Privilege Escalation (Last 5 Years)

```bash
python cve_scraper.py -k "linux kernel privilege escalation" -y 5
```

#### 2. Apache Vulnerabilities (Specific Date Range)

```bash
python cve_scraper.py -k "apache" -s "2023-01-01 00:00" -e "2024-12-31 23:59"
```

#### 3. Filter by CPE for Specific Products

```bash
python cve_scraper.py -k "kernel" -y 2 --cpe "cpe:2.3:o:linux:linux_kernel"
```

#### 4. Custom Output Filename

```bash
python cve_scraper.py -k "docker" -y 1 -o docker_vulnerabilities
```

#### 5. Export JSON Format Only

```bash
python cve_scraper.py -k "kubernetes" -y 2 --json-only
```

## 📁 Output Formats

### JSON Format
Structured data for programmatic processing:
```json
[
  {
    "CVE ID": "CVE-2024-1234",
    "Published Date": "2024-01-15T10:00:00",
    "Severity": "HIGH",
    "CVSS Score": 7.8,
    ...
  }
]
```

### CSV Format
Tabular data that can be opened directly in Excel for filtering and analysis.

### Markdown Format
Formatted report document for easy reading and sharing.

## 🔧 Advanced Usage

### Use as Python Module

```python
from cve_scraper import CVEScraper

# Create scraper instance
scraper = CVEScraper(api_key='YOUR_API_KEY')

# Execute search
results = scraper.scrape(
    keyword='linux kernel',
    start_date='2023-01-01 00:00',
    end_date='2024-12-31 23:59'
)

# Save results
scraper.save_all('my_results')
```

## ⚠️ Notes

1. **API Limitation**: NVD API limits single query time span to no more than 120 days, the script handles this automatically
2. **Rate Limits**: 
   - Without API key: Max 5 requests per 30 seconds
   - With API key: Max 50 requests per 30 seconds
3. **Network Requirements**: Need access to `services.nvd.nist.gov`
4. **Data Volume**: Large-scale queries may take considerable time, API key recommended

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🔗 Related Links

- [NVD Official Website](https://nvd.nist.gov/)
- [NVD API Documentation](https://nvd.nist.gov/developers)
- [nvdlib Library Documentation](https://nvdlib.com/)
- [CVSS Scoring Standard](https://www.first.org/cvss/)

---

**Disclaimer**: This tool is for security research and learning purposes only. Please comply with relevant laws and NVD terms of use.
