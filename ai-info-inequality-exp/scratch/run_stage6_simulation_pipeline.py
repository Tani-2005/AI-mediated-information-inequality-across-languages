import os
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

# Output directory for synthetic datasets and results
OUTPUT_DIR = "scratch/stage6_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/datasets", exist_ok=True)

MASTER_SEED = 20261003
np.random.seed(MASTER_SEED)

LATIN_SQUARE = {
    1: ["PMEGP", "PM_VISHWAKARMA", "PM_SVANIDHI"],
    2: ["PM_VISHWAKARMA", "PM_SVANIDHI", "PMEGP"],
    3: ["PM_SVANIDHI", "PMEGP", "PM_VISHWAKARMA"]
}

ARMS = ["ENGLISH_ONLY", "HINDI_ONLY", "CODE_SWITCHING"]

def generate_synthetic_dataset(world_id="world1", n_per_arm=48, planted_params=None, seed=42):
    np.random.seed(seed)
    
    if planted_params is None:
        planted_params = {}
        
    n_total = n_per_arm * 3 # 144 participants
    participant_ids = [f"p_{i+1:03d}" for i in range(n_total)]
    
    # 48 participants per arm
    arms_assignment = np.repeat(ARMS, n_per_arm)
    np.random.shuffle(arms_assignment) # randomized balance
    
    # AILS scores: continuous 12 to 60 (mean ~ 36, SD ~ 8)
    ails_scores = np.clip(np.random.normal(loc=36.0, scale=8.0, size=n_total).round(), 12, 60).astype(int)
    ails_mean = ails_scores.mean()
    ails_centered = ails_scores - ails_mean
    
    # Stratum assignment (<36 LOW, >=36 HIGH)
    strata = np.where(ails_scores < 36, "LOW", "HIGH")
    
    # Language Background (LEAP-Q)
    self_read_en = np.clip(np.random.normal(7.5, 1.5, n_total).round(), 1, 10)
    self_read_hi = np.clip(np.random.normal(7.0, 1.5, n_total).round(), 1, 10)
    lang_dominance = self_read_en - self_read_hi # -9 to +9
    
    # Latin Square task ordering (1, 2, or 3)
    order_ids = np.random.choice([1, 2, 3], size=n_total)
    
    # Participant random intercepts u_0i ~ N(0, tau^2)
    tau = planted_params.get("tau", 0.60)
    u_0i = np.random.normal(0, tau, size=n_total)
    
    rows = []
    
    # Default planted effects
    mu_base = planted_params.get("mu_base", 6.50)
    eff_english = planted_params.get("eff_english", 0.00)
    eff_cs = planted_params.get("eff_cs", 0.00)
    eff_hindi = planted_params.get("eff_hindi", 0.00)
    beta_ails = planted_params.get("beta_ails", 0.05)
    beta_int_en = planted_params.get("beta_int_en", 0.00)
    beta_int_cs = planted_params.get("beta_int_cs", 0.00)
    sigma_err = planted_params.get("sigma_err", 1.50)
    
    # Scenario effect defaults
    scen_effects = {"PMEGP": 0.0, "PM_VISHWAKARMA": -0.20, "PM_SVANIDHI": +0.20}
    pos_effects = {1: -0.10, 2: 0.0, 3: +0.10}
    
    for idx in range(n_total):
        p_id = participant_ids[idx]
        arm = arms_assignment[idx]
        ails_val = ails_scores[idx]
        ails_c = ails_centered[idx]
        stratum_val = strata[idx]
        dom_val = lang_dominance[idx]
        ord_id = order_ids[idx]
        u_i = u_0i[idx]
        
        task_list = LATIN_SQUARE[ord_id]
        
        for pos_idx, scenario in enumerate(task_list, start=1):
            # Calculate DecisionQuality score
            if arm == "ENGLISH_ONLY":
                arm_eff = eff_english
                int_eff = beta_int_en * ails_c
            elif arm == "CODE_SWITCHING":
                arm_eff = eff_cs
                int_eff = beta_int_cs * ails_c
            else: # HINDI_ONLY
                arm_eff = eff_hindi
                int_eff = 0.0
                
            det_scen = scen_effects[scenario]
            det_pos = pos_effects[pos_idx]
            
            # Planted DecisionQuality
            if world_id == "world4": # Bounded / Ceiling Effect World
                # Beta/Truncated normal distribution near 10.0
                raw_dq = mu_base + arm_eff + det_scen + det_pos + beta_ails * ails_c + int_eff + u_i + np.random.normal(0, sigma_err)
                dq = np.clip(raw_dq, 0.0, 10.0)
                if arm in ["ENGLISH_ONLY", "CODE_SWITCHING"]:
                    # Inject ceiling mass
                    if np.random.rand() < 0.35:
                        dq = 10.0
            else:
                raw_dq = mu_base + arm_eff + det_scen + det_pos + beta_ails * ails_c + int_eff + u_i + np.random.normal(0, sigma_err)
                dq = round(float(np.clip(raw_dq, 0.0, 10.0)), 2)
                
            # Process & Telemetry Variables
            if world_id == "world6": # Full Stress World
                # Overdispersed counts, zero-heavy clicks, speeding exclusions
                doc_clicks = int(np.random.negative_binomial(0.5, 0.2)) # overdispersed
                doc_duration = round(float(np.random.lognormal(mean=2.5, sigma=1.2)), 1)
                prompt_count = int(np.random.negative_binomial(1.0, 0.3)) + 1
                nasa_tlx = round(float(np.clip(np.random.normal(12.0 + (2.0 if arm=='HINDI_ONLY' else 0.0), 3.5), 1, 20)), 1)
                bias_prob = 0.04
                task_duration = round(float(np.random.uniform(20.0, 350.0)), 1)
                is_speeding = task_duration < 30.0
                leakage = bool(np.random.rand() < 0.08)
            else:
                # Standard realistic telemetry
                click_lambda = 4.5 if arm == "ENGLISH_ONLY" else (3.0 if arm == "HINDI_ONLY" else 4.0)
                doc_clicks = int(np.random.poisson(click_lambda))
                doc_duration = round(float(np.clip(np.random.lognormal(mean=3.2, sigma=0.6), 5.0, 250.0)), 1)
                prompt_count = int(np.random.poisson(2.5) + 1)
                nasa_tlx = round(float(np.clip(np.random.normal(10.0 + (2.5 if arm=='HINDI_ONLY' else 0.0), 2.5), 1, 20)), 1)
                
                # Automation bias probability
                if world_id == "world5": # Sparse events
                    bias_prob = 0.03 if arm == "ENGLISH_ONLY" else 0.06
                else:
                    bias_prob = 0.05 if arm == "ENGLISH_ONLY" else (0.15 if arm == "HINDI_ONLY" else 0.08)
                
                task_duration = round(float(np.random.normal(180.0, 45.0)), 1)
                is_speeding = False
                leakage = False
                
            auto_bias = 1 if np.random.rand() < bias_prob else 0
            confidence = int(np.clip(round(np.random.normal(5.0 + (dq - 6.5)*0.3, 1.2)), 1, 7))
            
            rows.append({
                "participant_id": p_id,
                "arm": arm,
                "ails_score": ails_val,
                "ails_centered": round(ails_c, 3),
                "stratum": stratum_val,
                "lang_dominance": dom_val,
                "order_id": ord_id,
                "scenario": scenario,
                "position": pos_idx,
                "decision_quality": dq,
                "doc_clicks": doc_clicks,
                "doc_duration": doc_duration,
                "prompt_count": prompt_count,
                "nasa_tlx": nasa_tlx,
                "automation_bias": auto_bias,
                "confidence": confidence,
                "task_duration_s": task_duration,
                "is_speeding": is_speeding,
                "language_leakage": leakage
            })
            
    df = pd.DataFrame(rows)
    return df

def run_simulation_pipeline(n_replicates=100):
    print(f"================================================================")
    print(f"RUNNING STAGE 6 MONTE CARLO SIMULATION PIPELINE ({n_replicates} REPLICATES)")
    print(f"================================================================")
    
    worlds_config = {
        "world1": {
            "name": "World 1 — Null World (Type-I Error Test)",
            "planted": {"mu_base": 6.50, "eff_english": 0.0, "eff_cs": 0.0, "eff_hindi": 0.0, "tau": 0.60, "sigma_err": 1.50}
        },
        "world2": {
            "name": "World 2 — H1/H2 Effect World (Planted Main Effects)",
            "planted": {"mu_base": 5.50, "eff_english": 1.50, "eff_cs": 1.20, "eff_hindi": 0.0, "tau": 0.60, "sigma_err": 1.50}
        },
        "world3": {
            "name": "World 3 — H3 Moderation World (Planted Interaction)",
            "planted": {"mu_base": 5.50, "eff_english": 1.20, "eff_cs": 1.00, "eff_hindi": 0.0, "beta_int_en": 0.08, "beta_int_cs": 0.05, "tau": 0.60, "sigma_err": 1.50}
        },
        "world4": {
            "name": "World 4 — Bounded / Ceiling World (Boundary Robustness)",
            "planted": {"mu_base": 7.50, "eff_english": 1.50, "eff_cs": 1.20, "eff_hindi": 0.0, "tau": 0.60, "sigma_err": 1.50}
        },
        "world5": {
            "name": "World 5 — Sparse Automation-Bias World (GLMM Separation Check)",
            "planted": {"mu_base": 6.50, "eff_english": 1.00, "eff_cs": 0.80, "eff_hindi": 0.0, "tau": 0.60, "sigma_err": 1.50}
        },
        "world6": {
            "name": "World 6 — Full Stress World (Overdispersion, Speeding & Leakage)",
            "planted": {"mu_base": 5.80, "eff_english": 1.40, "eff_cs": 1.10, "eff_hindi": 0.0, "tau": 0.60, "sigma_err": 1.50}
        }
    }
    
    summary_results = []
    
    for w_key, w_info in worlds_config.items():
        print(f"\n---> Simulating {w_info['name']}...")
        
        h1_estimates = []
        h1_pvals = []
        h1_cis = []
        
        h2_estimates = []
        h2_pvals = []
        h2_cis = []
        
        h3_pvals = []
        h3_estimates = []
        
        overdispersion_ratios = []
        nb_triggered_count = 0
        separation_count = 0
        speeding_excluded_count = 0
        
        # Save first replicate dataset to CSV
        df_rep0 = generate_synthetic_dataset(world_id=w_key, planted_params=w_info["planted"], seed=MASTER_SEED)
        df_rep0.to_csv(f"{OUTPUT_DIR}/datasets/{w_key}_sample.csv", index=False)
        
        for rep in range(n_replicates):
            seed = MASTER_SEED + rep
            df = generate_synthetic_dataset(world_id=w_key, planted_params=w_info["planted"], seed=seed)
            
            # Apply pre-registered speeding exclusion (<30s) if present
            if w_key == "world6":
                speeding_n = df["is_speeding"].sum()
                speeding_excluded_count += speeding_n
                df_clean = df[~df["is_speeding"]].copy()
            else:
                df_clean = df.copy()
                
            # Fit Primary LMM: decision_quality ~ C(arm, Treatment('HINDI_ONLY')) + C(scenario) + C(position)
            try:
                lmm_model = smf.mixedlm(
                    "decision_quality ~ C(arm, Treatment('HINDI_ONLY')) + C(scenario) + C(position)",
                    data=df_clean,
                    groups=df_clean["participant_id"]
                )
                lmm_fit = lmm_model.fit(reml=True)
                
                params = lmm_fit.params
                bse = lmm_fit.bse
                pvals = lmm_fit.pvalues
                
                # C1 Contrast: ENGLISH_ONLY - HINDI_ONLY
                en_key = "C(arm, Treatment('HINDI_ONLY'))[T.ENGLISH_ONLY]"
                if en_key in params:
                    c1_est = params[en_key]
                    c1_se = bse[en_key]
                    c1_p = pvals[en_key]
                    c1_ci = (c1_est - 1.96 * c1_se, c1_est + 1.96 * c1_se)
                else:
                    c1_est, c1_p, c1_ci = 0.0, 1.0, (0.0, 0.0)
                    
                # C2 Contrast: CODE_SWITCHING - HINDI_ONLY
                cs_key = "C(arm, Treatment('HINDI_ONLY'))[T.CODE_SWITCHING]"
                if cs_key in params:
                    c2_est = params[cs_key]
                    c2_se = bse[cs_key]
                    c2_p = pvals[cs_key]
                    c2_ci = (c2_est - 1.96 * c2_se, c2_est + 1.96 * c2_se)
                else:
                    c2_est, c2_p, c2_ci = 0.0, 1.0, (0.0, 0.0)
                    
                h1_estimates.append(c1_est)
                h1_pvals.append(c1_p)
                h1_cis.append(c1_ci)
                
                h2_estimates.append(c2_est)
                h2_pvals.append(c2_p)
                h2_cis.append(c2_ci)
                
            except Exception as e:
                pass
                
            # Fit Interactive LMM for H3
            try:
                lmm_h3 = smf.mixedlm(
                    "decision_quality ~ C(arm, Treatment('HINDI_ONLY')) * ails_centered + C(scenario) + C(position)",
                    data=df_clean,
                    groups=df_clean["participant_id"]
                )
                lmm_h3_fit = lmm_h3.fit(reml=True)
                int_key = "C(arm, Treatment('HINDI_ONLY'))[T.ENGLISH_ONLY]:ails_centered"
                if int_key in lmm_h3_fit.params:
                    h3_estimates.append(lmm_h3_fit.params[int_key])
                    h3_pvals.append(lmm_h3_fit.pvalues[int_key])
            except Exception:
                pass
                
            # Count Model Overdispersion Diagnostic (DocClicks)
            try:
                poisson_mod = smf.glm("doc_clicks ~ C(arm) + C(scenario) + C(position)", data=df_clean, family=sm.families.Poisson()).fit()
                pearson_chi2 = poisson_mod.pearson_chi2
                df_resid = poisson_mod.df_resid
                phi = pearson_chi2 / df_resid if df_resid > 0 else 1.0
                overdispersion_ratios.append(phi)
                if phi > 1.5:
                    nb_triggered_count += 1
            except Exception:
                pass
                
            # Logistic GLMM Separation Check (AutomationBias)
            try:
                logit_mod = smf.logit("automation_bias ~ C(arm)", data=df_clean).fit(disp=False)
                if any(logit_mod.bse > 8.0):
                    separation_count += 1
            except Exception:
                separation_count += 1
                
        # Calculate summary statistics across replicates
        planted_c1 = w_info["planted"].get("eff_english", 0.0) - w_info["planted"].get("eff_hindi", 0.0)
        planted_c2 = w_info["planted"].get("eff_cs", 0.0) - w_info["planted"].get("eff_hindi", 0.0)
        planted_h3 = w_info["planted"].get("beta_int_en", 0.0)
        
        mean_h1_est = np.mean(h1_estimates) if h1_estimates else 0.0
        bias_h1 = mean_h1_est - planted_c1
        rmse_h1 = np.sqrt(np.mean((np.array(h1_estimates) - planted_c1)**2)) if h1_estimates else 0.0
        power_h1 = np.mean([p < 0.05 for p in h1_pvals]) if h1_pvals else 0.0
        
        # 95% CI Coverage for H1
        coverage_h1 = np.mean([(ci[0] <= planted_c1 <= ci[1]) for ci in h1_cis]) if h1_cis else 0.0
        
        mean_h2_est = np.mean(h2_estimates) if h2_estimates else 0.0
        bias_h2 = mean_h2_est - planted_c2
        power_h2 = np.mean([p < 0.05 for p in h2_pvals]) if h2_pvals else 0.0
        
        mean_h3_est = np.mean(h3_estimates) if h3_estimates else 0.0
        power_h3 = np.mean([p < 0.05 for p in h3_pvals]) if h3_pvals else 0.0
        
        mean_phi = np.mean(overdispersion_ratios) if overdispersion_ratios else 1.0
        nb_trigger_pct = (nb_triggered_count / n_replicates) * 100
        
        summary_results.append({
            "world": w_key,
            "name": w_info["name"],
            "planted_c1": planted_c1,
            "est_c1": round(mean_h1_est, 3),
            "bias_c1": round(bias_h1, 3),
            "rmse_c1": round(rmse_h1, 3),
            "coverage_c1_pct": round(coverage_h1 * 100, 1),
            "power_c1_pct": round(power_h1 * 100, 1),
            "planted_c2": planted_c2,
            "est_c2": round(mean_h2_est, 3),
            "power_c2_pct": round(power_h2 * 100, 1),
            "planted_h3": planted_h3,
            "est_h3": round(mean_h3_est, 4),
            "power_h3_pct": round(power_h3 * 100, 1),
            "mean_dispersion_phi": round(mean_phi, 2),
            "nb_trigger_pct": round(nb_trigger_pct, 1),
            "separation_pct": round((separation_count / n_replicates) * 100, 1)
        })
        
    res_df = pd.DataFrame(summary_results)
    res_df.to_csv(f"{OUTPUT_DIR}/monte_carlo_summary.csv", index=False)
    
    print("\n================================================================")
    print("MONTE CARLO SIMULATION SUMMARY TABLE")
    print("================================================================")
    print(res_df.to_string(index=False))
    
    return res_df

if __name__ == "__main__":
    run_simulation_pipeline(n_replicates=5)
