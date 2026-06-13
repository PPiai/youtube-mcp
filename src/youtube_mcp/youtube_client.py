"""
YouTube Data API v3 Client
"""
import os
from typing import Any, Dict, List, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class YouTubeClient:
    """Client for YouTube Data API v3."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=api_key)
    
    def search_videos(
        self,
        query: str,
        max_results: int = 10,
        order: str = "relevance",
        published_after: Optional[str] = None,
        published_before: Optional[str] = None,
        region_code: Optional[str] = None,
        video_duration: Optional[str] = None,
        video_definition: Optional[str] = None,
        video_dimension: Optional[str] = None,
        video_license: Optional[str] = None,
        video_type: Optional[str] = None,
        channel_id: Optional[str] = None,
        topic_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search for videos on YouTube."""
        try:
            request = self.youtube.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=min(max_results, 50),
                order=order,
                publishedAfter=published_after,
                publishedBefore=published_before,
                regionCode=region_code,
                videoDuration=video_duration,
                videoDefinition=video_definition,
                videoDimension=video_dimension,
                videoLicense=video_license,
                videoType=video_type,
                channelId=channel_id,
                topicId=topic_id,
            )
            response = request.execute()
            return {"success": True, "data": response}
        except HttpError as e:
            return {"success": False, "error": str(e)}
    
    def search_channels(
        self,
        query: str,
        max_results: int = 10,
        order: str = "relevance",
    ) -> Dict[str, Any]:
        """Search for channels on YouTube."""
        try:
            request = self.youtube.search().list(
                part="snippet",
                q=query,
                type="channel",
                maxResults=min(max_results, 50),
                order=order,
            )
            response = request.execute()
            return {"success": True, "data": response}
        except HttpError as e:
            return {"success": False, "error": str(e)}
    
    def get_video_details(self, video_ids: List[str]) -> Dict[str, Any]:
        """Get detailed information about videos."""
        try:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics,status,topicDetails,recordingDetails",
                id=",".join(video_ids),
            )
            response = request.execute()
            return {"success": True, "data": response}
        except HttpError as e:
            return {"success": False, "error": str(e)}
    
    def get_channel_details(self, channel_ids: List[str]) -> Dict[str, Any]:
        """Get detailed information about channels."""
        try:
            request = self.youtube.channels().list(
                part="snippet,contentDetails,statistics,status,topicDetails,brandingSettings",
                id=",".join(channel_ids),
            )
            response = request.execute()
            return {"success": True, "data": response}
        except HttpError as e:
            return {"success": False, "error": str(e)}
    
    def get_trending_videos(
        self,
        region_code: str = "US",
        category_id: Optional[str] = None,
        max_results: int = 20,
    ) -> Dict[str, Any]:
        """Get trending videos for a region."""
        try:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                chart="mostPopular",
                regionCode=region_code,
                videoCategoryId=category_id,
                maxResults=min(max_results, 50),
            )
            response = request.execute()
            return {"success": True, "data": response}
        except HttpError as e:
            return {"success": False, "error": str(e)}
    
    def get_video_categories(self, region_code: str = "US") -> Dict[str, Any]:
        """Get video categories for a region."""
        try:
            request = self.youtube.videoCategories().list(
                part="snippet",
                regionCode=region_code,
            )
            response = request.execute()
            return {"success": True, "data": response}
        except HttpError as e:
            return {"success": False, "error": str(e)}
    
    def get_channel_videos(
        self,
        channel_id: str,
        max_results: int = 10,
        order: str = "date",
        published_after: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get videos from a specific channel."""
        try:
            # First get the channel's uploads playlist ID
            channel_response = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id,
            ).execute()
            
            if not channel_response.get("items"):
                return {"success": False, "error": "Channel not found"}
            
            uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            
            # Get videos from uploads playlist
            request = self.youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=min(max_results, 50),
            )
            response = request.execute()
            
            # Get video details
            video_ids = [item["contentDetails"]["videoId"] for item in response.get("items", [])]
            if video_ids:
                videos_response = self.get_video_details(video_ids)
                return {"success": True, "data": {"playlist_items": response, "videos": videos_response}}
            
            return {"success": True, "data": {"playlist_items": response, "videos": {"items": []}}}
        except HttpError as e:
            return {"success": False, "error": str(e)}
    
    def get_playlist_videos(
        self,
        playlist_id: str,
        max_results: int = 10,
    ) -> Dict[str, Any]:
        """Get videos from a playlist."""
        try:
            request = self.youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=min(max_results, 50),
            )
            response = request.execute()
            
            # Get video details
            video_ids = [item["contentDetails"]["videoId"] for item in response.get("items", [])]
            if video_ids:
                videos_response = self.get_video_details(video_ids)
                return {"success": True, "data": {"playlist_items": response, "videos": videos_response}}
            
            return {"success": True, "data": {"playlist_items": response, "videos": {"items": []}}}
        except HttpError as e:
            return {"success": False, "error": str(e)}
    
    def search_playlists(
        self,
        query: str,
        max_results: int = 10,
    ) -> Dict[str, Any]:
        """Search for playlists on YouTube."""
        try:
            request = self.youtube.search().list(
                part="snippet",
                q=query,
                type="playlist",
                maxResults=min(max_results, 50),
            )
            response = request.execute()
            return {"success": True, "data": response}
        except HttpError as e:
            return {"success": False, "error": str(e)}
    
    def get_comments(
        self,
        video_id: str,
        max_results: int = 20,
        order: str = "relevance",
    ) -> Dict[str, Any]:
        """Get comments for a video."""
        try:
            request = self.youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=min(max_results, 100),
                order=order,
            )
            response = request.execute()
            return {"success": True, "data": response}
        except HttpError as e:
            return {"success": False, "error": str(e)}
    
    def get_channel_by_handle(self, handle: str) -> Dict[str, Any]:
        """Get channel details by handle (@username)."""
        try:
            # Search for channel by handle
            request = self.youtube.search().list(
                part="snippet",
                q=handle,
                type="channel",
                maxResults=1,
            )
            response = request.execute()
            
            if not response.get("items"):
                return {"success": False, "error": "Channel not found"}
            
            channel_id = response["items"][0]["id"]["channelId"]
            return self.get_channel_details([channel_id])
        except HttpError as e:
            return {"success": False, "error": str(e)}