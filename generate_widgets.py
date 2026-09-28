import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('widgets', exist_ok=True)

banners = [
    {
        'id': 'thepathlab',
        'tag': 'METALS & POWERTRAIN',
        'title': 'ThePathLab',
        'desc': '9대 금속 시세 & 파워트레인',
        'accent': (56, 189, 248),  # #38bdf8
        'sub': 'thapathlab.com',
        'url': 'https://thapathlab.com/'
    },
    {
        'id': 'runanalyz',
        'tag': 'RUNNING DATA LAB',
        'title': 'RunAnalyz',
        'desc': '러닝 마일리지 & 94종 슈즈',
        'accent': (0, 242, 254),  # #00f2fe
        'sub': 'runanalyz.com',
        'url': 'https://runanalyz.com/'
    },
    {
        'id': 'bookinquiry',
        'tag': 'THINKING ENGINE',
        'title': 'BookInquiry',
        'desc': '목적 지향형 1:1 독서 사색',
        'accent': (245, 158, 11),  # #f59e0b
        'sub': 'bookinquiry.com',
        'url': 'https://bookinquiry.com/'
    },
    {
        'id': 'autocost',
        'tag': 'MOBILITY & RECALL',
        'title': 'AutoCost & Issue',
        'desc': '유가 유지비 & 리콜 인텔리전스',
        'accent': (16, 185, 129),  # #10b981
        'sub': 'thapathlab.com/autocost',
        'url': 'https://thapathlab.com/autocost/'
    },
    {
        'id': 'hub',
        'tag': 'OFFICIAL HUB',
        'title': '소장 Lab Hub',
        'desc': '전체 사이트 & 연구소 모음',
        'accent': (129, 140, 248),  # #818cf8
        'sub': 'thapathlab.com',
        'url': 'https://thapathlab.com/'
    }
]

W, H = 340, 210

font_tag = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 16)
font_title = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 26)
font_desc = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 17)
font_sub = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 15)
font_btn = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 16)

for b in banners:
    # 캔버스 배경 (#0F172A)
    img = Image.new('RGB', (W, H), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # 둥근 카드 테두리 (#334155)
    draw.rounded_rectangle([2, 2, W-3, H-3], radius=16, outline=(51, 65, 85), width=2)
    
    # 상단 컬러 포인트 바
    draw.rounded_rectangle([6, 6, W-7, 14], radius=4, fill=b['accent'])
    
    # 태그 / 카테고리
    draw.text((22, 26), b['tag'], font=font_tag, fill=b['accent'])
    
    # 메인 타이틀
    draw.text((22, 52), b['title'], font=font_title, fill=(255, 255, 255))
    
    # 설명
    draw.text((22, 92), b['desc'], font=font_desc, fill=(203, 213, 225))
    
    # 서브 도메인
    draw.text((22, 122), b['sub'], font=font_sub, fill=(100, 116, 139))
    
    # 하단 바로가기 버튼 박스
    btn_box = [22, 154, W-22, 196]
    draw.rounded_rectangle(btn_box, radius=8, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.text((36, 164), '서비스 바로가기', font=font_btn, fill=(241, 245, 249))
    draw.text((W-56, 163), '➔', font=font_btn, fill=b['accent'])
    
    out_path = f"widgets/banner_{b['id']}.png"
    img.save(out_path, quality=95)
    print(f"Generated {out_path}")

print("All banners generated successfully!")
