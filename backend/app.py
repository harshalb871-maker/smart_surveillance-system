import argparse
import cv2
from pathlib import Path
from detector import IntrusionDetector
from tracker import SimpleTracker
from behavior import BehaviorAnalyzer
from alert import AlertSystem


def parse_args():
    parser = argparse.ArgumentParser(description="Smart Surveillance System")
    parser.add_argument(
        "-s",
        "--source",
        default="0",
        help="Video source: webcam index (0,1,...) or file name/path (e.g. sample.mp4 or ../videos/sample.mp4)",
    )
    return parser.parse_args()


def resolve_source(source):
    if source.isdigit():
        return int(source)

    path = Path(source)
    if path.exists():
        return str(path)

    workspace_videos = Path(__file__).resolve().parent.parent / "videos"
    candidate = workspace_videos / source
    if candidate.exists():
        return str(candidate)

    candidate_cwd = Path.cwd() / source
    if candidate_cwd.exists():
        return str(candidate_cwd)

    candidate_cwd_videos = Path.cwd() / "videos" / source
    if candidate_cwd_videos.exists():
        return str(candidate_cwd_videos)

    return source


def main():
    args = parse_args()
    use_source = resolve_source(args.source)
    print("Starting Smart Surveillance System...")
    print(f"Using video source: {use_source}")

    # Initialize components
    detector = IntrusionDetector()
    tracker = SimpleTracker()
    behavior_analyzer = BehaviorAnalyzer()
    alert_system = AlertSystem()
    alerted_ids = set()

    cap = cv2.VideoCapture(use_source)

    if not cap.isOpened():
        print(f"Error: Could not open video source: {args.source}")
        return

    print("System is running. Press 'q' in the video window to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video stream.")
            break

        # 1. Object Detection (Find people in the frame)
        detections, annotated_frame = detector.detect(frame)

        # 2. Tracking (Keep track of objects over time)
        tracked_objects = tracker.update(detections)

        # 3. Behavior Analysis & Alerts
        for obj in tracked_objects:
            behavior = behavior_analyzer.analyze(obj["history"])
            if behavior != "Normal" and obj["id"] not in alerted_ids:
                alert_system.trigger_alert(behavior, frame)
                alerted_ids.add(obj["id"])

            x1, y1, x2, y2 = obj["box"]
            color = (0, 0, 255) if behavior != "Normal" else (0, 255, 0)
            label = f"ID {obj['id']}: {behavior}"
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                annotated_frame,
                label,
                (x1, max(20, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )

        # 4. Display the output
        cv2.imshow("Smart Surveillance System", annotated_frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting system...")
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
