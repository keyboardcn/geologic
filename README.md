# Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Usage
```bash
cd src
```
## general query
- python3 picture_search_cls.py -[option] args -[option] args

For example:
```bash
python3 picture_search_cls.py -filename Iceland.png -type png
```

will show:

``` code
['-type', 'png', '-filename', 'Iceland.png']
[PictureMetaCls(filename='Iceland.png', type='png', image_size=8.35, image_x=600, image_y=800, dpi=72, center_coordinate=None, favorite='', continent='', bit_color=None, alpha='', hockey_team='Team Iceland', user_tags='Johnson, Volcano, Dusk')]
```

## polygon query
```
python3 picture_search_cls.py -polygon '(51.129, -114.010), (50.742, -113.948), (50.748, -113.867)'
```