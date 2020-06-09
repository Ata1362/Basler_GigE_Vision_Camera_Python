# Install the Pylon lib using below code
# pip install pypylon-opencv-viewer
import cv2 as cv
from pypylon import pylon

# To convert raw array from Camera to OpenCV readable image.
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# Define the Camera you can find the S/N  
SN = 'Your camera Serial number'
info = None
# Search for available cameras on your Network
for cams in pylon.TlFactory.GetInstance().EnumerateDevices():
    if cams.GetSerialNumber() == SN:
        info = cams
        print('Camera with SN: {} is found'.format(SN))
        break
else:
    print('Camera with SN: {} is not visible on network'.format(SN))

# Call and activate the specific camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(info))
camera.Open()

# demonstrate some feature access
new_width = camera.Width.GetValue() - camera.Width.GetInc()
if new_width >= camera.Width.GetMin():
    camera.Width.SetValue(new_width)
# TO take a specific number of shots you can use below codes.
# NumberOfShots = 50
# camera.StartGrabbingMax(NumberOfShots)

camera.StartGrabbing()

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data.
        image = converter.Convert(grabResult)
        img = image.GetArray()
        cv.namedWindow('Basler Camera SN: {}'.format(SN), cv.WINDOW_NORMAL)
        cv.imshow('Basler Camera SN: {}'.format(SN), img)
        if cv.waitKey(5) & 0xff == ord("q"):
            break
    grabResult.Release()

cv.destroyWindow('Basler Camera SN: {}'.format(SN))
camera.Close()
