import os, cv2, math, imagehash, img2pdf, shutil, re
from PIL import Image
from progress.bar import Bar

def main():
    print("""
██████╗░██████╗░░█████╗░░██████╗░██╗░░██╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝░╚██╗██╔╝
██████╔╝██████╔╝██║░░██║██║░░██╗░░╚███╔╝░
██╔═══╝░██╔══██╗██║░░██║██║░░╚██╗░██╔██╗░
██║░░░░░██║░░██║╚█████╔╝╚██████╔╝██╔╝╚██╗
╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░╚═════╝░╚═╝░░╚═╝
=========================================
    Author: Mohamed Marzouk
    GitHub: https://github.com/MohamedMarzouk23
    LinkedIn: https://www.linkedin.com/in/109-marzouk
""")
    print("Please! Enter the full file name with the extension like v.mp4 / v.mkv / etc......")
    while True:
        fileName = input("File Name/Path: ")

        while not os.path.isfile(fileName):
            print("File name or path is invalid! please try again")
            fileName = input("File Name/Path: ")


        vidcap = cv2.VideoCapture(fileName)
        print("\n=================================")
        print(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

        bar = Bar('Processing', max=int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)), suffix='%(percent)d%%')

        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        successA, imageA = vidcap.read()
        imageAHash = imagehash.average_hash(Image.fromarray(imageA).convert("RGB"))
        
        workDir = 'imgs'
        if os.path.exists(workDir) and os.path.isdir(workDir):
            shutil.rmtree(workDir)
        os.mkdir("imgs")
        
        img_path = os.path.join(os.getcwd() , 'imgs')

        print()
        print(cv2.imwrite(os.path.join(img_path , r'1.jpg'), imageA))
        print(os.path.join(img_path , r'1.jpg'))
        imgs = [os.path.join(img_path , r'1.jpg')]

        count = 2
        while successA:
            frameId = vidcap.get(1)
            successB, imageB = vidcap.read()
            if (frameId % fps * 3 == 0):
                imageBHash = imagehash.average_hash(Image.fromarray(imageB).convert("RGB"))
                if imageAHash != imageBHash:
                    path = os.path.join(img_path , r'%d.jpg') % count
                    print()
                    print(cv2.imwrite(path, imageB))
                    print(path)
                    imgs.append(path)
                    count += 1
                imageAHash = imageBHash
            imageA = imageB
            successA = successB
            bar.next()

        if not os.path.exists('Results'):
            os.mkdir("Results")
        with open(os.path.join(os.getcwd(), r'Results\[ %s ] - result.pdf') % fileName, "ab") as f:
            f.write(img2pdf.convert(imgs))

        if os.path.exists(workDir) and os.path.isdir(workDir):
            shutil.rmtree(workDir)
        print("\nDone!")
        x = input("Another file? [y/n] => ")
        if x.upper() != "Y":
            break

if __name__ == "__main__":
    main()
