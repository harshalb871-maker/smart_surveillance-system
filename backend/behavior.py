import math
import os

class BehaviorAnalyzer:
    def __init__(self, model_path='../models/behavior_model.h5'):
        # In a real scenario, you'd load a Keras/TensorFlow model here:
        # import tensorflow as tf
        # self.model = tf.keras.models.load_model(model_path)
        print("Behavior model loaded (Mock Implementation).")

    def analyze(self, tracking_history):
        # Simple heuristic analysis based on movement history.
        if os.getenv("ALERT_TEST_MODE", "0") == "1":
            return "Suspicious (Test mode)"

        if not tracking_history or len(tracking_history) < 2:
            return "Normal"

        # Compute the last movement speed in pixels per frame.
        last_center = tracking_history[-1]
        previous_center = tracking_history[-2]
        delta_x = last_center[0] - previous_center[0]
        delta_y = last_center[1] - previous_center[1]
        speed = math.hypot(delta_x, delta_y)

        # Very fast movement may indicate suspicious or running behavior.
        if speed > 30:
            return "Suspicious (Fast movement)"

        # If the object has been present for several frames and barely moves,
        # treat that as loitering.
        if len(tracking_history) >= 5:
            total_distance = 0.0
            for i in range(-5, -1):
                total_distance += math.hypot(
                    tracking_history[i + 1][0] - tracking_history[i][0],
                    tracking_history[i + 1][1] - tracking_history[i][1],
                )
            average_speed = total_distance / 4.0
            if average_speed < 2.0:
                return "Suspicious (Loitering)"

        return "Normal"
