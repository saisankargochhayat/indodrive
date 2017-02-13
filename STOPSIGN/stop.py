import cv2
stop_cascade = cv2.CascadeClassifier('stop_sign.xml')
cap = cv2.VideoCapture(0)
a = 1
while 1:
    ret, image = cap.read()
    img = cv2.resize(image, (720, 480))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    signs = stop_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in signs:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        print('stop :' + str(a))
        a = a + 1

    cv2.imshow('img', img)
    # k = cv2.waitKey(30) & 0xff
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
