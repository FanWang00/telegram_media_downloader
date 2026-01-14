import yt_dlp

def download_videos_in_date_range(channel_url, start_date, end_date):
    
    def date_filter(info_dict, *, incomplete=False):
        # 1. Try to find the date in multiple possible fields
        video_date = info_dict.get('upload_date') or info_dict.get('release_date')
        
        # 2. If we still can't find a date, print details and skip
        if not video_date:
            title = info_dict.get('title', 'Unknown Title')
            url = info_dict.get('webpage_url', 'Unknown URL')
            print(f"\n[Skipping] No date found for: {title}\nLink: {url}\n")
            return 'No date found'
            
        # 3. Compare dates
        if video_date < start_date:
            return f'Video too old ({video_date})'
        if video_date > end_date:
            return f'Video too new ({video_date})'
            
        return None

    ydl_opts = {
        # Select 1080p (or best available up to 1080p)
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'merge_output_format': 'mp4',
        
        'match_filter': date_filter,
        'ignoreerrors': True,
        'outtmpl': '%(upload_date)s - %(title)s.%(ext)s',
        
        # 4. IGNORE LIVE STREAMS (Optional)
        # Often live streams are the cause of "No Date" errors. 
        # Uncomment the line below to skip them automatically:
        # 'match_filter': yt_dlp.utils.match_filter_func("!is_live"), 
    }

    print(f"Starting download for videos between {start_date} and {end_date}...")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([channel_url])
# --- CONFIGURATION ---
if __name__ == "__main__":
    # 1. Put the channel URL here (works with /videos, /streams, or user URLs)
    CHANNEL_URL = "https://www.youtube.com/@ChinaBabeTV/videos" 
    
    # 2. Set your date range (Format: YYYYMMDD)
    START_DATE = "20250101" # Jan 1st, 2023
    END_DATE   = "20260112" # Dec 31st, 2023

    download_videos_in_date_range(CHANNEL_URL, START_DATE, END_DATE)