export interface MapPoint {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
}

export function formatMapLabel(point: MapPoint) {
  return `${point.name} (${point.latitude.toFixed(2)}, ${point.longitude.toFixed(2)})`;
}
