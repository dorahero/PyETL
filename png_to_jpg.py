
from PIL import Image
import os.path
import glob
# , width=150, height=150
def convertjpg(jpgfile, outdir):
    img = Image.open(jpgfile)
    try:
        # new_img = img.resize((width, height), Image.BILINEAR)
        image = img.convert("RGB")
        j = jpgfile[:-3] + 'jpg'
        if not os.path.exists(outdir + '/{}'.format(jpgfile.split('\\')[1])):
            os.makedirs(outdir + '/{}'.format(jpgfile.split('\\')[1], exist_ok=True))

        image.save(os.path.join(outdir + '/{}'.format(jpgfile.split('\\')[1]), os.path.basename(j)))
        try:
            os.remove(jpgfile)
        except OSError as e:
            print(e)
    except Exception as e:
        print('1')
        print(e)


files = glob.glob("./png/*/*.png")
for i, jpgfile in enumerate(files):
    if i % (int(len(files)/10)) == 0:
        print(round(i*100/len(files), 1), '%')
    convertjpg(jpgfile, "./jpg")
    # print(jpgfile)
