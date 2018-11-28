# -*- coding: utf-8 -*-

import os
import math
from tkinter import *
from tkinter.filedialog import askdirectory
from PIL import Image

class circlePicture():

    def __init__(self, path, outdir):
        self.path = path.strip()
        self.outdir = outdir.strip()
        self.tmpdir = self.outdir +'\\tmp'
        if not os.path.exists(self.outdir):
            os.mkdir(self.outdir)
        if not os.path.exists(self.tmpdir):
            os.mkdir(self.tmpdir)
    
    def check_image_with_pil(self, path):
        try:
            Image.open(path)
        except IOError:
            return False
        return True
    
    def walk_pic(self):
        pathname = []
        for (dirpath, dirnames, filenames) in os.walk(self.path):       
            for filename in filenames:
                fullpath = os.path.join(dirpath, filename)
                if dirpath == self.path and self.check_image_with_pil(fullpath):
                    pathname += [fullpath]
        return pathname
    
    def circle(self, f, newf):
        image = Image.open(f).convert('RGBA')
        size = image.size
        r2 = min(size[0], size[1])
        # if r2 > 600:
        r2 = 200
        # if size[0] != size[1]:
            # image = image.resize((r2, r2), Image.ANTIALIAS)
        image = image.resize((r2, r2), Image.ANTIALIAS)
        r3 = 100
        imagenew = Image.new('RGBA', (r3*2, r3*2), (255,255,255,0))
        pimold = image.load()
        pimnew = imagenew.load()
        r = float(r2/2)
        for i in range(r2):
            for j in range(r2):
                lx = abs(i - r)
                ly = abs(j - r)
                l = (pow(lx, 2) + pow(ly, 2))**0.5
                if l < r3:
                    pimnew[i - (r - r3), j - (r - r3)] = pimold[i, j]
        imagenew.save(newf)

    def arrangeImagesInCircle(self, masterImage, imagesToArrange):
        imgWidth, imgHeight = masterImage.size
        diameter = min(
            imgWidth  - max(img.size[0] for img in imagesToArrange),
            imgHeight - max(img.size[1] for img in imagesToArrange)
        )
        radius = diameter / 2
        circleCenterX = imgWidth / 2
        circleCenterY = imgHeight / 2
        theta = 2 * math.pi / len(imagesToArrange)
        for i in range(len(imagesToArrange)):
            curImg = imagesToArrange[i]
            angle = i * theta
            dx = int(radius * math.cos(angle))
            dy = int(radius * math.sin(angle))
            pos = (
                int(circleCenterX + dx - curImg.size[0]/2 ),
                int(circleCenterY + dy - curImg.size[1]/2 )
            )
            masterImage.paste(curImg, pos)
            
    def removedir(self, path):
        for file in os.listdir(path):   
            targetFile = os.path.join(path, file)   
            if os.path.isfile(targetFile):   
                os.remove(targetFile)
        os.rmdir(path)

    def doCircle(self):
        pathname = self.walk_pic()
        count = 0
        imageFilenames = []
        for f in pathname:
            newf = (self.tmpdir + '\\' + str(count) + '.png')
            self.circle(f, newf)
            imageFilenames.append(newf)
            count += 1
        n = len(imageFilenames)
        r = 200
        pic_d = math.ceil( r * math.cos(math.pi/n)/math.sin(math.pi/n) + 2 * r)
        img = Image.new("RGB", (pic_d, pic_d), (255, 255, 255))
        images = [Image.open(filename) for filename in imageFilenames]
        self.arrangeImagesInCircle(img, images) 
        img.save((self.outdir + "\\output.png"))
        self.removedir(self.tmpdir)            

def selectPath():
    path_ = askdirectory()
    inpath.set(path_)

def outputPath():
    path_ = inpath.get()
    outdir = os.path.join(path_ , 'out')
    find = circlePicture(path_, outdir)
    find.doCircle()
    outpath.set(outdir)
        
if __name__ == '__main__':

    root = Tk()
    root.title("制作圆形图")
       
    inpath = StringVar()
    outpath = StringVar()
    Label(root, text = "图片文件夹").grid(row = 0, column = 0)
    Entry(root, textvariable=inpath).grid(row = 0, column = 1)
    Button(root, text="路径选择", command=selectPath).grid(row = 0, column = 2)
    Label(root, text = "输出文件夹").grid(row = 1, column = 0)
    Entry(root, textvariable=outpath).grid(row = 1, column = 1)
    Button(root, text="执行", command=outputPath).grid(row = 1, column = 2)
    
    root.mainloop()