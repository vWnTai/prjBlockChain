export type User = { username: string; role: "Admin" | "Analyst" | "Viewer" };
export type Config = {
  seed: number;
  wallet_count: number;
  transaction_count: number;
  simulation_days: number;
  block_interval_seconds: number;
  max_transactions_per_block: number;
  patterns: string[];
};
export type Run = {
  id: string;
  seed: number;
  config: Config;
  status: string;
  transaction_count: number;
  analyzed_count: number;
  analysis_version: string;
  created_at: string;
  error: string | null;
  analyses?: {
    version: string;
    status: string;
    kind: string;
    mode: string;
    job_id: string;
    error: string | null;
  }[];
};
export type Hit = {
  code: string;
  anchor: string;
  evidence: string[];
  observed: Record<string, unknown>;
  thresholds: Record<string, unknown>;
  rule_version: string;
};
export type Assessment = {
  score: number;
  severity: string;
  components: Record<"E" | "P" | "V" | "Q" | "A", number>;
  blend: number;
  floors: Record<string, number>;
  hits: Hit[];
  coverage: string;
  partial_reasons: string[];
  model_status: string;
  analysis_mode: string;
};
export type Tx = {
  tx_hash: string;
  from_address: string;
  to_address: string;
  value_base: string;
  fee_base: string;
  timestamp: string;
  global_index: number;
  block_height: number;
  tx_index: number;
  assessment: Assessment | null;
};
export type Alert = Hit & {
  id: string;
  run_id: string;
  detector_code: string;
  score: number;
  severity: string;
  status: string;
  revision: number;
  detected_at: string;
  detected_order: number;
  last_detected_order?: number;
  analysis_version: string;
  coverage: string;
  assessment: Assessment;
  transactions?: Tx[];
  reviews?: {
    username: string;
    status: string;
    old_status: string;
    comment: string;
    created_at: string;
  }[];
};
export type ClassMetric = {
  TP: number;
  FP: number;
  FN: number;
  TN: number;
  precision: number | null;
  recall: number | null;
  FPR: number | null;
  F1: number | null;
};
export type Metrics = {
  status?: string;
  scope: string;
  transaction_count?: number;
  online?: ClassMetric;
  sequential_with_retrospective_feed?: ClassMetric;
  analysis_mode?: string;
  retrospective?: ClassMetric;
  patterns?: Record<
    string,
    {
      online?: ClassMetric;
      sequential_with_retrospective_feed?: ClassMetric;
      retrospective: ClassMetric;
      campaign_detected: boolean;
      core_overlap: number;
    }
  >;
  campaign_count?: number;
  campaigns_detected?: number;
  alerts_by_detector?: Record<string, number>;
  alerts_per_1000_tx?: number;
  analysis_seconds?: number;
  throughput_tx_s?: number;
  process_p95_ms?: number;
  partial_assessments?: number;
  ledger_hash?: string;
  analysis_version?: string;
};
export type GraphData = {
  nodes: {
    id: string;
    label: string;
    score: number | null;
    severity: string;
    blacklisted: boolean;
    coverage: string;
  }[];
  edges: {
    id: string;
    source: string;
    target: string;
    value_base: string;
    fee_base: string;
    block_height: number;
    tx_index: number;
    timestamp: string;
    global_index: number;
    tx_hash: string;
  }[];
  truncated: boolean;
  analysis_mode?: string;
  coverage: string;
  as_of_index: number;
  analysis_version: string;
};
export type GraphParams = {
  center?: string;
  hops?: number;
  as_of_index?: number;
  alert_id?: string;
  analysis_version?: string;
};
