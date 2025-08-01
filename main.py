import requests
import concurrent.futures
from json import dumps
from country_codes import con_codes
from time import time
from typing import Dict, List, Tuple, Optional


class iTunesCountryChecker:
    """
    A class to check iTunes app availability across different countries concurrently.
    """
    
    def __init__(self, am_id: int, max_workers: int = 92, timeout: int = 6):
        """
        Initialize the iTunes Country Checker.
        
        Args:
            am_id: iTunes app ID to check
            max_workers: Maximum number of concurrent threads
            timeout: Request timeout in seconds
        """
        self.am_id = am_id
        self.max_workers = max_workers
        self.timeout = timeout
        self.session = None
        self._setup_session()
    
    def _setup_session(self) -> None:
        """Setup requests session with optimized connection pooling."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'KVT_AM_CountryChecker/1.0)',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate'
        })
        
        # Configure connection pooling
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=100,
            pool_maxsize=100,
            max_retries=requests.adapters.Retry(
                total=2,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504]
            )
        )
        self.session.mount('https://', adapter)
    
    def _check_country(self, code_country_pair: Tuple[str, str]) -> Tuple[str, bool]:
        code, country = code_country_pair
        try:
            response = self.session.get(
                f"https://itunes.apple.com/lookup?id={self.am_id}&country={code}",
                timeout=self.timeout
            )
            if response.status_code == 200:
                data = response.json()
                has_results = data.get("resultCount", 0) > 0
                return f"{country} ({code})", has_results
            else:
                return f"{country} ({code})", False
        except Exception:
            return f"{country} ({code})", False
    
    def check_countries(self, countries: Optional[Dict[str, str]] = None) -> Dict:
        if countries is None:
            countries = con_codes
        
        start_time = time()
        available_countries = []
        unavailable_countries = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(self._check_country, countries.items())
            
            for country_info, is_available in results:
                if is_available:
                    available_countries.append(country_info)
                else:
                    unavailable_countries.append(country_info)
        
        end_time = time()
        
        return {
            "am_id": self.am_id,
            "duration_seconds": round(end_time - start_time, 4),
            "total_countries_checked": len(available_countries) + len(unavailable_countries),
            "available_in_countries": sorted(available_countries),
            "available_not_in_countries": sorted(unavailable_countries)
        }
    
    def check_and_print_json(self, countries: Optional[Dict[str, str]] = None) -> str:
        result = self.check_countries(countries)
        json_result = dumps(result, indent=4, ensure_ascii=False)
        print(json_result)
        return json_result
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup session."""
        self.close()
    
    def close(self) -> None:
        """Close the session and cleanup resources."""
        if self.session:
            self.session.close()
            self.session = None


# if __name__ == "__main__":
#     # OOP approach with context manager
#     with iTunesCountryChecker(1822254656) as checker:
#         checker.check_and_print_json()