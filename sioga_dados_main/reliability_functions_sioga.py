import pandas as pd
from reliability.Fitters import Fit_Weibull_2P
from reliability.Distributions import Weibull_Distribution

def calculate_mtbf(data):
    data["data falha"] = pd.to_datetime(data["data falha"])
    data["data inicio operacao"] = pd.to_datetime(data["data inicio operacao"])
    data["mtbf"] = (data["data falha"] - data["data inicio operacao"]).dt.days
    return data

def resample_mtbf(data):
    if (data["situacao"] == "failure").sum() == 1:
        data_espelho = data.copy()
        data_espelho["mtbf"] = data_espelho["mtbf"] * 1.01
        data = pd.concat([data, data_espelho])
        return data
    
def calcular_distribuicao_weibull(alpha, beta, alpha_lower, beta_lower, alpha_upper, beta_upper):
    weibull = Weibull_Distribution(alpha=alpha, beta=beta)
    weibull_lower = Weibull_Distribution(alpha=alpha_lower, beta=beta_lower)
    weibull_upper = Weibull_Distribution(alpha=alpha_upper, beta=beta_upper)

    # Calcular as variáveis para a distribuição Weibull
    result = {
        "alpha": alpha,
        "beta": beta,
        "reliability_weibull": weibull.SF(show_plot=False).tolist(),
        "hazard_function_weibull": weibull.HF(show_plot=False).tolist(),
        "chf_weibull": weibull.CHF(show_plot=False).tolist(),
        "cdf_weibull": weibull.CDF(show_plot=False).tolist(),
        "pdf_weibull": weibull.PDF(show_plot=False).tolist(),
        "RUL_weibull": [weibull.mean_residual_life(t=i) for i in range(200)],
        "alpha_lower": alpha_lower,
        "beta_lower": beta_lower,
        "reliability_weibull_lower": weibull_lower.SF(show_plot=False).tolist(),
        "hazard_function_weibull_lower": weibull_lower.HF(show_plot=False).tolist(),
        "chf_weibull_lower": weibull_lower.CHF(show_plot=False).tolist(),
        "cdf_weibull_lower": weibull_lower.CDF(show_plot=False).tolist(),
        "pdf_weibull_lower": weibull_lower.PDF(show_plot=False).tolist(),
        "RUL_weibull_lower": [weibull_lower.mean_residual_life(t=i) for i in range(200)],
        "alpha_upper": alpha_upper,
        "beta_upper": beta_upper,
        "reliability_weibull_upper": weibull_upper.SF(show_plot=False).tolist(),
        "hazard_function_weibull_upper": weibull_upper.HF(show_plot=False).tolist(),
        "chf_weibull_upper": weibull_upper.CHF(show_plot=False).tolist(),
        "cdf_weibull_upper": weibull_upper.CDF(show_plot=False).tolist(),
        "pdf_weibull_upper": weibull_upper.PDF(show_plot=False).tolist(),
        "RUL_weibull_upper": [weibull_upper.mean_residual_life(t=i) for i in range(200)]
    }
    
    return result

def calculate_weibull_params(data):
    data = calculate_mtbf(data)
    data = resample_mtbf(data)

    censored = data.query("situacao == 'operating'")
    non_censored = data.query("situacao == 'failure'")
    fit = Fit_Weibull_2P(failures=non_censored["mtbf"].tolist(), 
                        right_censored=censored["mtbf"].tolist(), 
                        show_probability_plot=False) 

    alpha = fit.alpha
    beta = fit.beta
    alpha_lower = fit.alpha_lower
    alpha_upper = fit.alpha_upper
    beta_lower = fit.beta_lower
    beta_upper = fit.beta_upper

    json_answer = calcular_distribuicao_weibull(alpha, beta, alpha_lower, beta_lower, alpha_upper, beta_upper)
    print(json_answer)
    return json_answer