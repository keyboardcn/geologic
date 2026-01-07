from picture_meta_cls import PictureMetaCls, value_props, str_props, Point
import re
from copy import deepcopy
import sys
class PictureSearchCls:
    metas = []
    def __init__(self, meta_file='./geologic_sample.csv'):
        with open(meta_file, "r") as f:
            n = 0
            for line in f:
                if n == 0: 
                    n += 1
                    continue
                pattern1 =  r'\"\"\"(.*?)\"\"\"'
                user_tags = re.findall(pattern1, line)
                user_tags = user_tags[0] if len(user_tags) else None
                line = re.sub(pattern1, '', line)
                
                pattern2 =  r'\"(.*?)\"'
                cor = re.findall(pattern2, line)
                cor = cor[0] if len(cor) else None
                line = re.sub(pattern2, '', line)

                row = line.split(',')
                meta = PictureMetaCls(
                    filename = row[0],
                    type = row[1],
                    image_size = float(row[2]) if row[2] else None,
                    image_x = int(row[3]) if row[3] else None,
                    image_y = int(row[4]) if row[4] else None,
                    dpi = int(row[5]) if row[5] else None,
                    
                    center_coordinate = self.transfer(cor),
                    favorite = row[7],
                    continent = row[8],
                    bit_color = int(row[9]) if row[9] else None,
                    alpha = row[10],
                    hockey_team = row[11],
                    user_tags = user_tags
                )
                self.metas.append(meta)

    def filter(self, args):
        rst_metas = [True] * len(self.metas)
        try:
            while args:
                cmd = args.pop(0)
                if cmd[0] != '-':
                    raise Exception('Command should lead with -')
                cmd = cmd[1:]
                value = args.pop(0) 
                if cmd in str_props:
                    rst_metas = self.str_cmd_filter(cmd, value, rst_metas)
                elif cmd in value_props:
                    rst_metas = self.value_cmd_filter(cmd, value, rst_metas)
                elif cmd == 'polygon':
                    rst_metas = self.polygon_filter(value, rst_metas)
                else:
                    raise Exception('Command not found')
            output = [self.metas[i] for i, m in enumerate(rst_metas) if m]
            print(output)
            return output
        except e as e:
            raise e

    def polygon_filter(self, value: str, rst_metas):
        poly = self.str2tuple_array(value)
        if len(poly) <3:
            raise Exception('Ploy must have three vertex')
        return [ self.pnpoly(poly, m.center_coordinate) \
             for i, m in enumerate(self.metas) if rst_metas[i]]
    
    def pnpoly(self, poly: list[Point], center_coordinate):
        if not center_coordinate:
            return False
        (pointx, pointy) = center_coordinate
        inside = False
        j = len(poly) - 1
        for i in range(len(poly)):
            if ((poly[i].y > pointy) != (poly[j].y > pointy)
                and (
                    pointx
                    < (poly[j].x - poly[i].x)
                    * (pointy - poly[i].y)
                    / (poly[j].y - poly[i].y)
                    + poly[i].x
                )
            ):
                inside = not inside
            j = i

        return inside    

    
    def str2tuple_array(self, value: str) -> list[Point]:
        nums = list(map(float, value.replace('(', '').replace(')','').split(',')))
        points = []
        for i in range(0, len(nums), 2):
            points.append(Point(
                x = nums[i],
                y = nums[i+1]
            ))
        return points

    def str_cmd_filter(self, cmd: str, value: str, rst_metas):
        return [value in dict(m)[cmd] for i, m in enumerate(self.metas) if rst_metas[i]]

    def value_cmd_filter(self, cmd: str, value: str, rst_metas):
        return [ eval(f'{dict(m)[cmd]} {value}') for i, m in enumerate(self.metas) if rst_metas[i]]
    
    def transfer(self, cor: str|None) -> tuple[float, float]:
        if not cor:
            return None
        x, y = cor.split(',')
        if 'N' in x or 'S' in x:
            x1 = self.dms2dd(x)
            y1 = self.dms2dd(y)
            return (x1, y1)
        else:
            return (float(x), float(y))
        
    def dms2dd(self, x: str):
        '''
        :param x: dms lat or long
        :type x: str
        '''
        deg, minutes, direction = re.split('[°\'"]+', x)
        dd = (float(deg) + float(minutes)/60 + float(0)/(60*60))
        if 'W' in direction or 'S' in direction:
            dd *= -1
        return dd
    
if __name__ == "__main__":
    args = sys.argv[1:]
    print(args)
    p_cls = PictureSearchCls()
    p_cls.filter(args)
