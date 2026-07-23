import math

class SimpleTracker:
    def __init__(self, max_distance=80, max_lost=5):
        self.tracks = {}
        self.next_id = 0
        self.max_distance = max_distance
        self.max_lost = max_lost

    def update(self, detections):
        current_centers = []
        for det in detections:
            x1, y1, x2, y2 = det['box']
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            current_centers.append((det, (cx, cy)))

        assigned = set()
        for track_id, track in list(self.tracks.items()):
            best_index = None
            best_distance = math.inf
            for index, (_, center) in enumerate(current_centers):
                if index in assigned:
                    continue
                distance = math.hypot(center[0] - track['center'][0], center[1] - track['center'][1])
                if distance < best_distance:
                    best_distance = distance
                    best_index = index

            if best_index is not None and best_distance < self.max_distance:
                det, center = current_centers[best_index]
                assigned.add(best_index)
                track['box'] = det['box']
                track['center'] = center
                track['history'].append(center)
                track['history'] = track['history'][-20:]
                track['lost'] = 0
                track['frames'] += 1
                track['updated'] = True
            else:
                track['lost'] += 1
                track['updated'] = False

        for index, (det, center) in enumerate(current_centers):
            if index in assigned:
                continue
            self.tracks[self.next_id] = {
                'id': self.next_id,
                'box': det['box'],
                'center': center,
                'history': [center],
                'lost': 0,
                'frames': 1,
                'updated': True,
            }
            self.next_id += 1

        expired = [track_id for track_id, track in self.tracks.items() if track['lost'] > self.max_lost]
        for track_id in expired:
            del self.tracks[track_id]

        tracked_objects = []
        for track in self.tracks.values():
            tracked_objects.append({
                'id': track['id'],
                'box': track['box'],
                'center': track['center'],
                'history': track['history'],
                'frames': track['frames'],
                'updated': track['updated'],
            })

        return tracked_objects
