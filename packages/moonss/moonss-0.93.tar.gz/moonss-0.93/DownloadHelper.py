import json
import os
from bgeditor.common.utils import get_dir, download_file
from gbackup import DriverHelper
import uuid
import requests

def get_proxy_iproyal():
    proxy_tmp = f"http://victor69:dota2hoabt2@geo.iproyal.com:12321"
    proxies = {"http": proxy_tmp, "https": proxy_tmp}
    return proxies

def get_download_nwm_tiktok(url, retries=3):
    try:
        video_id=url.split('/')[-1]
        urld = f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}"
        proxies=get_proxy_iproyal()
        headers={'user-agent':'com.ss.android.ugc.trill/494+Mozilla/5.0+(Linux;+Android+12;+2112123G+Build/SKQ1.211006.001;+wv)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Version/4.0+Chrome/107.0.5304.105+Mobile+Safari/537.36'}
        res=requests.get(urld, headers=headers, proxies=proxies).json()
        # print(res)
        data=res['aweme_list'][0]
        nwm_video_url_HQ= data['video']['bit_rate'][0]['play_addr']['url_list'][0]
        return nwm_video_url_HQ
    except:
        if retries > 1:
            return get_download_nwm_tiktok(url,retries-1)
        pass
    return None

def download_ytdlp(videoId):
    videoId = videoId.strip()
    result = os.path.join(get_dir("download"), f"{videoId}.webm")
    cmd = f"yt-dlp -f bv+ba/b -o {result} {videoId}"
    print(cmd)
    rs= os.system(cmd)
    print(rs)
    return result

def download_tiktok_video(video_url):
    download_url = get_download_nwm_tiktok(video_url)
    return download_file(download_url,None,"mp4")
def download_douyin_video(video_id):
    return download_file(f"https://aweme.snssdk.com/aweme/v1/play/?video_id={video_id}&ratio=1080p&line=0",None, "mp4")
def donwload_instagram_video(crawl_data_txt):
    crawl_data = json.loads(crawl_data_txt)
    if "video_url" in crawl_data:
        return download_file(crawl_data['video_url'],None, "mp4")
    else:
        return None