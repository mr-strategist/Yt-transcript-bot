import re
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'(?:shorts\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_info(video_id):
    try:
        yt = YouTube(f'https://youtube.com/watch?v={video_id}')
        info = f"""
📽️ Video Information:
Title: {yt.title}
Channel: {yt.author}
Views: {yt.views:,}
Length: {yt.length} seconds
Published: {yt.publish_date.strftime('%Y-%m-%d')}
"""
        return info
    except:
        return None

def detect_chapters(transcript_text):
    patterns = [
        r'\d{1,2}:\d{2}\s+[-–]\s+.+',
        r'Chapter\s+\d+',
        r'Part\s+\d+'
    ]
    chapters = []
    for line in transcript_text.split('\n'):
        if any(re.match(p, line) for p in patterns):
            chapters.append(line)
    return chapters 
