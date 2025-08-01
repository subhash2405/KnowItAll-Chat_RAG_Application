from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

def extract_youtube_transcript(video):
    """
    Extracts the transcript of a YouTube video using its video ID.

    Args:
        video_id (str): The YouTube video ID.

    Returns:
        str: The transcript of the YouTube video.
    """
    try:
        video_id = video.split("v=")[-1].split("&")[0]  # Extract video ID from URL
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript = ""
        for item in transcript_list:
            transcript += item['text'] + " "
        # print(transcript)

    except TranscriptsDisabled:
        print("Transcripts are disabled for this video.")
        transcript = []
    
    return transcript

# print(extract_youtube_transcript("ncw1VYwyLBU"))