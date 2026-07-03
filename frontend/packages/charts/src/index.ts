export interface ChartPoint {
  label: string;
  value: number;
}

export function createSparklineData(values: number[]) {
  return values.map((value, index) => ({ label: `P${index + 1}`, value }));
}
