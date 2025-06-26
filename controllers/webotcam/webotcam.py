from controller import Robot
import numpy as np
import cv2

robot = Robot()
timestep = 64

camera = robot.getDevice('camera')
camera.enable(timestep)
camera.recognitionEnable(timestep)

while robot.step(timestep//32) != -1:
    # Get image and recognition objects
    img_data = camera.getImage()
    width = camera.getWidth()
    height = camera.getHeight()
    objects = camera.getRecognitionObjects()

    # Convert Webots image to OpenCV (BGRA → BGR)
    image = np.frombuffer(img_data, np.uint8).reshape((height, width, 4))
    bgr_image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    # Draw bounding boxes and model labels
    for obj in objects:
        # Get bounding box in image coordinates
        x, y = obj.position_on_image  # ✅ no parentheses
        w, h = obj.size_on_image      # ✅ no parentheses
        model_name = obj.model        # ✅ also a property


        # Calculate top-left and bottom-right corners
        top_left = (int(x - w / 2), int(y - h / 2))
        bottom_right = (int(x + w / 2), int(y + h / 2))

        # Draw rectangle
        cv2.rectangle(bgr_image, top_left, bottom_right, (0, 255, 0), 2)

        # Draw label above the box
        label_position = (top_left[0], top_left[1] - 10)
        cv2.putText(bgr_image, model_name, label_position,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Show the image in a window (must be running with GUI, not headless)
    cv2.imshow("Webots Object Detection", bgr_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
