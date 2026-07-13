from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse
import os

# Initialize with your active Scrapfly API Key
SCRAPFLY_API_KEY = os.environ.get('API_KEY', '')
client = ScrapflyClient(key=SCRAPFLY_API_KEY)

def extract_x_profile_data(profile_url: str):
    """
    Fetches raw unblocked data from an X profile page via Scrapfly 
    and uses AI-assisted extraction to grab Name, Handle, Bio, Location, and Comments safely.
    """
    print(f"📡 Querying Scrapfly API for: {profile_url}...")
    
    # UPDATED: Added explicit instructions for 'name' and 'handle'
    ai_extraction_prompt = (
        "Extract the user's main profile display name text as 'name', "
        "their account handle or username text (starting with @) as 'handle', "
        "the user profile biography text as 'bio', "
        "and an array of their latest 4 recent posts or comments text as 'comments'."
    )
    
    config = ScrapeConfig(
        url=profile_url,
        asp=True,                 # Bypasses X's active anti-scraping blocks
        render_js=True,           # Executes dynamic JavaScript layers
        country="us",             # Routes through premium US residential proxies
        wait_for_selector="body", # Avoids timing out on missing tweet UI selectors
        extraction_prompt=ai_extraction_prompt
    )
    
    # Clean up proxy warning by ensuring sticky proxies are not implicitly requested
    config.session_sticky_proxy = False 
    
    try:
        # Fire raw request
        response: ScrapeApiResponse = client.scrape(config)
        
        # FIX: Access the underlying scrape_result dictionary matrix payload safely
        result_json = response.scrape_result
        
        if "extracted_data" in result_json and "data" in result_json["extracted_data"]:
            return result_json["extracted_data"]["data"]
        else:
            print("⚠️ Warning: Scrapfly bypassed the block, but extraction dictionary structure was empty.")
            # UPDATED: Included default empty values for the new fields
            return {"name": "", "handle": "", "bio": "", "comments": []}

    except Exception as e:
        print(f"🚨 Connection failed: {str(e)}")
        return None

# --- Verification Run ---
if __name__ == "__main__":
    # Test execution using the precise profile link
    payload = extract_x_profile_data("https://x.com/elonmusk")
    print("\n📦 Fetch Output Data Payload:", payload)