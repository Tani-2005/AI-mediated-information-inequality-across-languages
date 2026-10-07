import os
import sys
import numpy as np
import pandas as pd
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

OUTPUT_DIR = "scratch/stage8_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MASTER_SEED = 20261003
ARMS = ["ENGLISH_ONLY", "HINDI_ONLY", "CODE_SWITCHING"]
LATIN_SQUARE = {
    1: ["PMEGP", "PM_VISHWAKARMA", "PM_SVANIDHI"],
    2: ["PM_VISHWAKARMA", "PM_SVANIDHI", "PMEGP"],
    3: ["PM_SVANIDHI", "PMEGP", "PM_VISHWAKARMA"]
}

def wilson_ci(k, n, confidence=0.95):
    if n == 0: return 0.0, 0.0, 0.0
    p = k / n
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    denominator = 1 + z**2 / n
    centre_adjusted = p + z**2 / (2 * n)
    adjusted_error = z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n)
    lower = (centre_adjusted - adjusted_error) / denominator
    upper = (centre_adjusted + adjusted_error) / denominator
    return p, max(0.0, lower), min(1.0, upper)

def generate_single_dataset(seed, n_per_arm=48, eff_en=0.0, eff_cs=0.0, eff_hi=0.0, 
                             beta_int_en=0.0, beta_int_cs=0.0, tau=0.60, sigma_err=1.50,
                             ceiling_mass=0.0, discrete_scoring=False,
                             attrition_type="MCAR", dropout_rate=0.0,
                             leakage_rate=0.0, auto_bias_p=(0.05, 0.05, 0.05)):
    np.random.seed(seed)
    n_total = n_per_arm * 3
    participant_ids = [f"p_{i+1:03d}" for i in range(n_total)]
    arms = np.repeat(ARMS, n_per_arm)
    
    ails_raw = np.clip(np.random.normal(36.0, 8.0, n_total).round(), 12, 60).astype(int)
    ails_c = ails_raw - ails_raw.mean()
    
    order_ids = np.random.choice([1, 2, 3], size=n_total)
    u_0i = np.random.normal(0, tau, size=n_total)
    
    rows = []
    scen_eff = {"PMEGP": 0.0, "PM_VISHWAKARMA": -0.20, "PM_SVANIDHI": +0.20}
    pos_eff = {1: -0.10, 2: 0.0, 3: +0.10}
    
    for idx in range(n_total):
        p_id = participant_ids[idx]
        arm = arms[idx]
        ails_val = ails_raw[idx]
        ac_val = ails_c[idx]
        u_i = u_0i[idx]
        ord_id = order_ids[idx]
        
        if arm == "ENGLISH_ONLY":
            a_eff, int_eff, p_bias = eff_en, beta_int_en * ac_val, auto_bias_p[0]
        elif arm == "CODE_SWITCHING":
            a_eff, int_eff, p_bias = eff_cs, beta_int_cs * ac_val, auto_bias_p[1]
        else:
            a_eff, int_eff, p_bias = eff_hi, 0.0, auto_bias_p[2]
            
        task_list = LATIN_SQUARE[ord_id]
        
        p_dropout = dropout_rate
        if attrition_type == "LANG_DEPENDENT" and arm == "HINDI_ONLY":
            p_dropout += 0.15
        elif attrition_type == "AILS_DEPENDENT" and ails_val < 36:
            p_dropout += 0.15
        elif attrition_type == "COMBINED":
            if arm == "HINDI_ONLY": p_dropout += 0.10
            if ails_val < 36: p_dropout += 0.10
            
        if np.random.rand() < p_dropout:
            continue
            
        for pos_idx, scenario in enumerate(task_list, start=1):
            base_val = 6.50 + a_eff + scen_eff[scenario] + pos_eff[pos_idx] + 0.05 * ac_val + int_eff + u_i
            err = np.random.normal(0, sigma_err)
            
            if discrete_scoring:
                raw_score = base_val + err
                steps = np.array([0.0, 2.5, 5.0, 7.5, 10.0])
                dq = steps[np.argmin(np.abs(steps - raw_score))]
            elif ceiling_mass > 0 and arm in ["ENGLISH_ONLY", "CODE_SWITCHING"] and np.random.rand() < ceiling_mass:
                dq = 10.0
            else:
                dq = round(float(np.clip(base_val + err, 0.0, 10.0)), 2)
                
            clicks = int(np.random.poisson(4.0 if arm != "HINDI_ONLY" else 2.5))
            dur = round(float(np.clip(np.random.lognormal(3.2, 0.6), 5.0, 250.0)), 1)
            prompts = int(np.random.poisson(2.5) + 1)
            tlx = round(float(np.clip(np.random.normal(10.0 + (2.5 if arm=="HINDI_ONLY" else 0.0), 2.5), 1, 20)), 1)
            bias_evt = 1 if np.random.rand() < p_bias else 0
            
            task_dur = round(float(np.random.normal(180.0, 45.0)), 1)
            is_speeding = task_dur < 30.0
            leakage = bool(np.random.rand() < leakage_rate)
            
            rows.append({
                "participant_id": p_id,
                "arm": arm,
                "ails_score": ails_val,
                "ails_centered": round(ac_val, 3),
                "scenario": scenario,
                "position": pos_idx,
                "decision_quality": dq,
                "doc_clicks": clicks,
                "doc_duration": dur,
                "prompt_count": prompts,
                "nasa_tlx": tlx,
                "automation_bias": bias_evt,
                "task_duration_s": task_dur,
                "is_speeding": is_speeding,
                "language_leakage": leakage
            })
            
    return pd.DataFrame(rows)

def run_h3_single(seed, beta_int):
    import statsmodels.formula.api as smf
    df = generate_single_dataset(seed=seed, eff_en=1.20, eff_cs=1.00, beta_int_en=beta_int)
    try:
        mod = smf.mixedlm("decision_quality ~ C(arm, Treatment('HINDI_ONLY')) * ails_centered + C(scenario) + C(position)", data=df, groups=df["participant_id"])
        res = mod.fit(reml=True, disp=False)
        b = res.params.get("C(arm, Treatment('HINDI_ONLY'))[T.ENGLISH_ONLY]:ails_centered", 0.0)
        se = res.bse.get("C(arm, Treatment('HINDI_ONLY'))[T.ENGLISH_ONLY]:ails_centered", 0.0)
        p = res.pvalues.get("C(arm, Treatment('HINDI_ONLY'))[T.ENGLISH_ONLY]:ails_centered", 1.0)
        return {"b": b, "se": se, "p": p, "success": True}
    except Exception:
        return {"b": 0.0, "se": 0.0, "p": 1.0, "success": False}

def run_stage8_additions():
    print("Executing Stage 8 specific simulations (World 4 beta=0.09, World 7 Overdispersion, World 9 Speeding/Leakage)...", flush=True)
    
    # 1. World 4 beta=0.09 (200 fast reps)
    results = []
    for r in range(200):
        res = run_h3_single(MASTER_SEED + 25000 + r, 0.09)
        results.append(res)
        
    valid = [r for r in results if r["success"]]
    b_vals = [r["b"] for r in valid]
    se_vals = [r["se"] for r in valid]
    p_vals = [r["p"] for r in valid]
    mean_b = np.mean(b_vals)
    bias = mean_b - 0.09
    rmse = np.sqrt(np.mean((np.array(b_vals) - 0.09)**2))
    covers = [(b - 1.96*se <= 0.09 <= b + 1.96*se) for b, se in zip(b_vals, se_vals)]
    pows = [p < 0.05 for p in p_vals]
    cov_p, cov_l, cov_h = wilson_ci(sum(covers), len(covers))
    pow_p, pow_l, pow_h = wilson_ci(sum(pows), len(pows))
    
    res_df = pd.DataFrame([{
        "beta_interaction": 0.09,
        "Empirical_Power_pct": f"{pow_p*100:.1f}% [{pow_l*100:.1f}%-{pow_h*100:.1f}%]",
        "Planted_beta": 0.09,
        "Estimated_beta": round(mean_b, 4),
        "Bias": round(bias, 4),
        "RMSE": round(rmse, 4),
        "CI_Coverage_pct": f"{cov_p*100:.1f}% [{cov_l*100:.1f}%-{cov_h*100:.1f}%]"
    }])
    res_df.to_csv(f"{OUTPUT_DIR}/h3_beta_009.csv", index=False)
    print(f"World 4 beta=0.09 Power: {pow_p*100:.1f}% [{pow_l*100:.1f}%-{pow_h*100:.1f}%], Estimated beta: {mean_b:.4f}", flush=True)

    # 2. World 9 Speeding and Leakage Audit
    df_leak = generate_single_dataset(seed=MASTER_SEED+9000, leakage_rate=0.08)
    n_init = len(df_leak)
    n_speeding = df_leak["is_speeding"].sum()
    n_leakage = df_leak["language_leakage"].sum()
    df_clean = df_leak[(~df_leak["is_speeding"]) & (~df_leak["language_leakage"])]
    n_clean = len(df_clean)
    
    leak_df = pd.DataFrame([{
        "Initial_Obs": n_init,
        "Speeding_Flagged": n_speeding,
        "Leakage_Flagged": n_leakage,
        "Clean_Obs": n_clean,
        "Exclusion_Rate_pct": f"{((n_init - n_clean)/n_init)*100:.1f}%"
    }])
    leak_df.to_csv(f"{OUTPUT_DIR}/world9_speeding_leakage.csv", index=False)
    print(f"World 9 Speeding/Leakage: Initial={n_init}, Speeding={n_speeding}, Leakage={n_leakage}, Clean={n_clean}", flush=True)

if __name__ == "__main__":
    run_stage8_additions()
