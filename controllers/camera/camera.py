from controller import Robot
from ultralytics import YOLO
import numpy as np
import cv2

# Initialize robot and camera
robot = Robot()
timestep = int(robot.getBasicTimeStep())

camera = robot.getDevice("camera")
camera.enable(64)

# Load pre-trained YOLOv8 model
model = YOLO("yolov8n.pt")

# Define HSV ranges for common colors
color_ranges = {
    "Red":    ([0, 120, 70], [10, 255, 255]),
    "Red2":   ([170, 120, 70], [180, 255, 255]),  # Wrap-around red
    "Green":  ([40, 40, 40], [80, 255, 255]),
    "Blue":   ([110, 50, 50], [130, 255, 255]),
    "Yellow": ([20, 100, 100], [30, 255, 255]),
}

def get_dominant_color(cropped_img):
    hsv = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
    color_scores = {}

    for color_name, (lower, upper) in color_ranges.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(hsv, lower, upper)
        score = cv2.countNonZero(mask)
        if score > 0:
            color_scores[color_name] = score

    if color_scores:
        dominant = max(color_scores, key=color_scores.get)
        if dominant == "Red2":
            return "Red"
        elif dominant.startswith("Red"):
            return "Red"
        return dominant
    return "Unknown"

def get_shape(contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(peri, 0.04 * peri, True)
    if len(approx) == 3:
        return "triangle"
    elif len(approx) == 4:
        return "rectangle"
    elif len(approx) > 6:
        return "circle"
    else:
        return "unknown"

while robot.step(32) != -1:
    width = camera.getWidth()
    height = camera.getHeight()
    image_data = camera.getImageArray()

    if image_data:
        # Convert to OpenCV format
        img_array = np.array(image_data, dtype=np.uint8)
        frame = img_array.reshape((height, width, 3))
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Run YOLO inference
        results = model(frame_bgr)

        annotated_frame = frame_bgr.copy()

        for r in results:
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0].to(int).tolist()
                x1, y1, x2, y2 = b
                x1, y1, x2, y2 = max(0, x1), max(0, y1), min(width, x2), min(height, y2)
                cls = int(box.cls[0])
                obj_label = model.names[cls]

                # Crop the detected object
                cropped_obj = frame_bgr[y1:y2, x1:x2]

                # Get dominant color
                color = get_dominant_color(cropped_obj)

                # Convert to grayscale + threshold for shape detection
                gray = cv2.cvtColor(cropped_obj, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if len(contours) > 0:
                    shape = get_shape(max(contours, key=cv2.contourArea))
                else:
                    shape = "unknown"

                # Build label
                final_label = ""
                if color != "Unknown" and shape != "unknown":
                    final_label = f"{color} {shape}"
                elif color != "Unknown":
                    final_label = color
                elif shape != "unknown":
                    final_label = shape
                else:
                    final_label = obj_label  # Fallback to object class name

                # Draw bounding box and label
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_frame, final_label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Show output
        cv2.imshow("Webots Camera - YOLO + Color + Shape", annotated_frame)
        cv2.waitKey(1)