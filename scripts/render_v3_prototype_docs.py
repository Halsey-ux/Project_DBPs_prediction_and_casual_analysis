from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / 'docs'
OUTPUT_DIR = PROJECT_ROOT / 'data_local' / 'V3_Chapter1_Part1_Prototype_Build'
V2_OUTPUT_DIR = PROJECT_ROOT / 'data_local' / 'V2_Chapter1_Part1_DBP_Data_Foundation'

SOURCE_SPECS = [
    ('tthm', 'TTHM', '\u7ed3\u679c\u53d8\u91cf', '_ug_l'),
    ('haa5', 'HAA5', '\u7ed3\u679c\u53d8\u91cf', '_ug_l'),
    ('ph', 'pH', '\u6838\u5fc3\u673a\u5236\u53d8\u91cf', ''),
    ('alkalinity', '\u603b\u78b1\u5ea6', '\u6838\u5fc3\u673a\u5236\u53d8\u91cf', '_mg_l'),
    ('toc', 'TOC', '\u6838\u5fc3\u673a\u5236\u53d8\u91cf', '_mg_l'),
    ('free_chlorine', '\u6e38\u79bb\u4f59\u6c2f', '\u6838\u5fc3\u673a\u5236\u53d8\u91cf', '_mg_l'),
    ('total_chlorine', '\u603b\u6c2f', '\u6269\u5c55\u673a\u5236\u53d8\u91cf', '_mg_l'),
    ('doc', 'DOC', '\u6269\u5c55\u673a\u5236\u53d8\u91cf', '_mg_l'),
    ('suva', 'SUVA', '\u6269\u5c55\u673a\u5236\u53d8\u91cf', '_l_mg_m'),
    ('uv254', 'UV254', '\u6269\u5c55\u673a\u5236\u53d8\u91cf', '_cm_inv'),
    ('chloramine', '\u6c2f\u80fa', '\u6269\u5c55\u673a\u5236\u53d8\u91cf', '_mg_l'),
]

HIGH_RISK_KEYS = {'tthm', 'haa5'}


def now_text() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def md_table(frame: pd.DataFrame) -> str:
    display = frame.copy().fillna('')
    headers = [str(column) for column in display.columns]
    lines = [
        '| ' + ' | '.join(headers) + ' |',
        '| ' + ' | '.join(['---'] * len(headers)) + ' |',
    ]
    for row in display.itertuples(index=False, name=None):
        lines.append('| ' + ' | '.join(str(value) for value in row) + ' |')
    return '\n'.join(lines)


def write_markdown(path: Path, lines: list[str]) -> None:
    normalized = []
    for line in lines:
        normalized.append(line.encode("utf-8").decode("unicode_escape") if "\\u" in line else line)
    path.write_text('\n'.join(normalized) + '\n', encoding='utf-8')


def make_records() -> tuple[pd.DataFrame, pd.DataFrame]:
    facility_rows = []
    for field_name, reason in [
        ('pwsid', '\u7cfb\u7edf\u7ea7 join \u4e3b\u952e\u3002'),
        ('water_facility_id', '\u4fdd\u7559\u8bbe\u65bd\u5f02\u8d28\u6027\u3002'),
        ('year', '\u56fa\u5b9a\u5e74\u5ea6\u7c92\u5ea6\u3002'),
        ('month', '\u56fa\u5b9a\u6708\u5ea6\u7c92\u5ea6\u3002'),
    ]:
        facility_rows.append({'\u5b57\u6bb5\u540d': field_name, '\u5b57\u6bb5\u7c7b\u522b': '\u4e3b\u952e', '\u6765\u6e90': '\u7edf\u4e00\u4e3b\u952e', '\u6784\u5efa\u65b9\u5f0f': '\u6807\u51c6\u5316\u4fdd\u7559', '\u4fdd\u7559\u7406\u7531': reason})
    for field_name, reason in [
        ('state_code', '\u4fbf\u4e8e\u5dde\u9645\u5dee\u5f02\u5206\u6790\u3002'),
        ('system_name', '\u4fbf\u4e8e\u56de\u67e5\u548c\u5199\u4f5c\u3002'),
        ('system_type', '\u53cd\u6620\u7cfb\u7edf\u7c7b\u578b\u5dee\u5f02\u3002'),
        ('source_water_type', '\u53cd\u6620\u6c34\u6e90\u7c7b\u578b\u5dee\u5f02\u3002'),
        ('water_facility_type', '\u533a\u5206 TP/DS \u7b49\u8bbe\u65bd\u89d2\u8272\u3002'),
        ('retail_population_served', '\u4fdd\u7559\u4eba\u53e3\u89c4\u6a21\u4fe1\u606f\u3002'),
        ('adjusted_total_population_served', '\u4fdd\u7559\u8c03\u6574\u540e\u4eba\u53e3\u89c4\u6a21\u4fe1\u606f\u3002'),
    ]:
        facility_rows.append({'\u5b57\u6bb5\u540d': field_name, '\u5b57\u6bb5\u7c7b\u522b': '\u7ed3\u6784\u80cc\u666f\u5b57\u6bb5', '\u6765\u6e90': 'treatment + occurrence fallback', '\u6784\u5efa\u65b9\u5f0f': '\u7ef4\u8868 join \u6216\u56de\u586b', '\u4fdd\u7559\u7406\u7531': reason})
    stat_reason = {
        'n_samples': '\u4fdd\u7559\u6837\u672c\u91cf\uff0c\u7528\u4e8e\u540e\u7eed\u52a0\u6743\u4e0e\u8d28\u63a7\u3002',
        'mean': '\u4e8c\u5c42\u4e3b\u5206\u6790\u7684\u4e3b\u8981\u5f3a\u5ea6\u6307\u6807\u3002',
        'median': '\u964d\u4f4e\u5f02\u5e38\u503c\u5f71\u54cd\u3002',
        'max': '\u4fdd\u7559\u5c3e\u90e8\u98ce\u9669\u4fe1\u606f\u3002',
        'p90': '\u4fdd\u7559\u53f3\u5c3e\u6d53\u5ea6\u7ed3\u6784\u3002',
    }
    for key, _label, category, suffix in SOURCE_SPECS:
        for stat_name in ['n_samples', 'mean', 'median', 'max', 'p90']:
            field_name = f'{key}_n_samples' if stat_name == 'n_samples' else f'{key}_{stat_name}{suffix}'
            facility_rows.append({'\u5b57\u6bb5\u540d': field_name, '\u5b57\u6bb5\u7c7b\u522b': f'{category}\u5b57\u6bb5', '\u6765\u6e90': f'{key}_facility_month', '\u6784\u5efa\u65b9\u5f0f': '\u6708\u5ea6\u805a\u5408', '\u4fdd\u7559\u7406\u7531': stat_reason[stat_name]})
    for field_name, reason in [
        ('has_water_system_facility_record', '\u6807\u8bb0\u662f\u5426\u53ef\u63a5\u5165\u7ed3\u6784\u5c42\u3002'),
        ('has_facility_plant_record', '\u6807\u8bb0\u662f\u5426\u6709\u5382\u7ea7\u5de5\u827a\u4fe1\u606f\u3002'),
        ('has_treatment_process_record', '\u6807\u8bb0\u662f\u5426\u6709\u5de5\u827a\u8fc7\u7a0b\u4fe1\u606f\u3002'),
        ('has_flow_record', '\u6807\u8bb0\u662f\u5426\u6709 flow \u4fe1\u606f\u3002'),
        ('treatment_process_record_count', '\u53cd\u6620\u5de5\u827a\u8bb0\u5f55\u4e30\u5bcc\u5ea6\u3002'),
        ('n_treatment_process_names', '\u53cd\u6620\u5de5\u827a\u79cd\u7c7b\u6570\u91cf\u3002'),
        ('n_treatment_objective_names', '\u53cd\u6620\u5de5\u827a\u76ee\u6807\u79cd\u7c7b\u6570\u91cf\u3002'),
        ('treatment_process_name_list', '\u4fdd\u7559\u5de5\u827a\u540d\u79f0\u6e05\u5355\u3002'),
        ('treatment_objective_name_list', '\u4fdd\u7559\u5de5\u827a\u76ee\u6807\u6e05\u5355\u3002'),
        ('filter_type_list', '\u4fdd\u7559\u8fc7\u6ee4\u7c7b\u578b\u6458\u8981\u3002'),
        ('plant_disinfectant_concentration_mean_mg_l', '\u4fdd\u7559\u6d88\u6bd2\u5242\u6d53\u5ea6\u7ed3\u6784\u7ebf\u7d22\u3002'),
        ('plant_ct_value_mean', '\u4fdd\u7559 CT \u7ed3\u6784\u6458\u8981\u3002'),
        ('flow_record_count', '\u53cd\u6620\u8bbe\u65bd\u8fde\u63a5\u89c4\u6a21\u3002'),
        ('n_supplying_facilities', '\u53cd\u6620\u8bbe\u65bd\u4e0a\u6e38\u590d\u6742\u5ea6\u3002'),
        ('has_disinfection_process', '\u662f\u5426\u5b58\u5728\u6d88\u6bd2\u5de5\u827a\u3002'),
        ('has_filtration_process', '\u662f\u5426\u5b58\u5728\u8fc7\u6ee4\u5de5\u827a\u3002'),
        ('has_adsorption_process', '\u662f\u5426\u5b58\u5728\u5438\u9644\u5de5\u827a\u3002'),
        ('has_oxidation_process', '\u662f\u5426\u5b58\u5728\u6c27\u5316\u5de5\u827a\u3002'),
        ('has_chloramination_process', '\u662f\u5426\u5b58\u5728\u6c2f\u80fa\u5316\u5de5\u827a\u3002'),
        ('has_hypochlorination_process', '\u662f\u5426\u5b58\u5728\u6b21\u6c2f\u5316\u5de5\u827a\u3002'),
        ('treatment_process_summary', '\u4fdd\u7559\u77ed\u6458\u8981\u3002'),
    ]:
        facility_rows.append({'\u5b57\u6bb5\u540d': field_name, '\u5b57\u6bb5\u7c7b\u522b': 'treatment \u6458\u8981\u5b57\u6bb5', '\u6765\u6e90': 'treatment \u76f8\u5173\u8868', '\u6784\u5efa\u65b9\u5f0f': '\u8bbe\u65bd\u5c42\u805a\u5408\u540e\u5916\u8fde\u63a5', '\u4fdd\u7559\u7406\u7531': reason})
    for field_name, reason in [
        ('has_tthm', '\u6807\u8bb0\u5f53\u524d\u884c\u662f\u5426\u6709 TTHM \u7ed3\u679c\u3002'),
        ('has_haa5', '\u6807\u8bb0\u5f53\u524d\u884c\u662f\u5426\u6709 HAA5 \u7ed3\u679c\u3002'),
        ('n_result_vars_available', '\u7edf\u8ba1\u7ed3\u679c\u53d8\u91cf\u53ef\u7528\u6570\u91cf\u3002'),
        ('n_core_vars_available', '\u7edf\u8ba1\u6838\u5fc3\u53d8\u91cf\u53ef\u7528\u6570\u91cf\u3002'),
        ('n_extended_vars_available', '\u7edf\u8ba1\u6269\u5c55\u53d8\u91cf\u53ef\u7528\u6570\u91cf\u3002'),
        ('n_mechanism_vars_available', '\u6c47\u603b\u673a\u5236\u53d8\u91cf\u8986\u76d6\u5f3a\u5ea6\u3002'),
        ('has_treatment_summary', '\u6807\u8bb0 treatment \u6458\u8981\u662f\u5426\u53ef\u7528\u3002'),
        ('source_module_count', '\u7edf\u8ba1\u5f53\u524d\u884c\u88ab\u591a\u5c11\u6a21\u5757\u8986\u76d6\u3002'),
        ('is_tthm_high_risk_month', '\u5feb\u901f\u6807\u8bb0 TTHM \u9ad8\u98ce\u9669\u6708\u3002'),
        ('is_haa5_high_risk_month', '\u5feb\u901f\u6807\u8bb0 HAA5 \u9ad8\u98ce\u9669\u6708\u3002'),
        ('match_quality_tier', '\u6309\u7ed3\u679c\u4e0e\u6838\u5fc3\u53d8\u91cf\u91cd\u5408\u5ea6\u5206\u5c42\u3002'),
    ]:
        facility_rows.append({'\u5b57\u6bb5\u540d': field_name, '\u5b57\u6bb5\u7c7b\u522b': '\u8d28\u91cf\u63a7\u5236\u5b57\u6bb5', '\u6765\u6e90': '\u6d3e\u751f', '\u6784\u5efa\u65b9\u5f0f': '\u4e3b\u8868\u5408\u5e76\u540e\u6d3e\u751f', '\u4fdd\u7559\u7406\u7531': reason})

    year_rows = []
    for field_name, reason in [('pwsid', '\u5168\u56fd\u7cfb\u7edf\u7ea7\u4e3b\u952e\u3002'), ('year', '\u5e74\u5ea6\u4e3b\u952e\u3002')]:
        year_rows.append({'\u5b57\u6bb5\u540d': field_name, '\u5b57\u6bb5\u7c7b\u522b': '\u4e3b\u952e', '\u6765\u6e90': 'V3_facility_month_master', '\u6784\u5efa\u65b9\u5f0f': '\u4ece\u4e8c\u5c42\u4e3b\u8868\u4e0a\u5377', '\u4fdd\u7559\u7406\u7531': reason})
    for field_name, role, reason in [
        ('state_code', '\u7ed3\u6784\u80cc\u666f\u5b57\u6bb5', '\u4fbf\u4e8e\u5dde\u9645\u5dee\u5f02\u5206\u6790\u3002'),
        ('system_name', '\u7ed3\u6784\u80cc\u666f\u5b57\u6bb5', '\u4fbf\u4e8e\u56de\u67e5\u3002'),
        ('system_type', '\u7ed3\u6784\u80cc\u666f\u5b57\u6bb5', '\u53cd\u6620\u7cfb\u7edf\u7c7b\u578b\u5dee\u5f02\u3002'),
        ('source_water_type', '\u7ed3\u6784\u80cc\u666f\u5b57\u6bb5', '\u53cd\u6620\u6c34\u6e90\u7c7b\u578b\u5dee\u5f02\u3002'),
        ('retail_population_served', '\u7ed3\u6784\u80cc\u666f\u5b57\u6bb5', '\u4fdd\u7559\u4eba\u53e3\u89c4\u6a21\u3002'),
        ('adjusted_total_population_served', '\u7ed3\u6784\u80cc\u666f\u5b57\u6bb5', '\u4fdd\u7559\u8c03\u6574\u540e\u4eba\u53e3\u89c4\u6a21\u3002'),
        ('n_facility_month_rows', '\u8d28\u91cf\u63a7\u5236\u5b57\u6bb5', '\u53cd\u6620\u5f53\u5e74\u8986\u76d6\u7684\u8bbe\u65bd-\u6708\u4efd\u5355\u5143\u6570\u3002'),
        ('months_observed_any', '\u8d28\u91cf\u63a7\u5236\u5b57\u6bb5', '\u53cd\u6620\u5f53\u5e74\u6709\u4efb\u610f\u6570\u636e\u7684\u6708\u4efd\u6570\u3002'),
        ('n_facilities_in_master', '\u7ed3\u6784\u80cc\u666f\u5b57\u6bb5', '\u53cd\u6620\u5f53\u5e74\u53c2\u4e0e\u805a\u5408\u7684\u8bbe\u65bd\u6570\u3002'),
        ('n_facilities_with_treatment_summary', 'treatment \u6458\u8981\u5b57\u6bb5', '\u53cd\u6620\u53ef\u63a5\u5165 treatment \u6458\u8981\u7684\u8bbe\u65bd\u6570\u3002'),
        ('water_facility_type_list', '\u7ed3\u6784\u80cc\u666f\u5b57\u6bb5', '\u6458\u8981\u8bbe\u65bd\u7c7b\u578b\u3002'),
        ('filter_type_list', 'treatment \u6458\u8981\u5b57\u6bb5', '\u6458\u8981\u8fc7\u6ee4\u7c7b\u578b\u3002'),
        ('treatment_process_name_list', 'treatment \u6458\u8981\u5b57\u6bb5', '\u6458\u8981\u5de5\u827a\u540d\u79f0\u3002'),
        ('treatment_objective_name_list', 'treatment \u6458\u8981\u5b57\u6bb5', '\u6458\u8981\u5de5\u827a\u76ee\u6807\u3002'),
        ('has_disinfection_process', 'treatment \u6458\u8981\u5b57\u6bb5', '\u662f\u5426\u5b58\u5728\u6d88\u6bd2\u5de5\u827a\u3002'),
        ('has_filtration_process', 'treatment \u6458\u8981\u5b57\u6bb5', '\u662f\u5426\u5b58\u5728\u8fc7\u6ee4\u5de5\u827a\u3002'),
        ('has_adsorption_process', 'treatment \u6458\u8981\u5b57\u6bb5', '\u662f\u5426\u5b58\u5728\u5438\u9644\u5de5\u827a\u3002'),
        ('has_oxidation_process', 'treatment \u6458\u8981\u5b57\u6bb5', '\u662f\u5426\u5b58\u5728\u6c27\u5316\u5de5\u827a\u3002'),
        ('has_chloramination_process', 'treatment \u6458\u8981\u5b57\u6bb5', '\u662f\u5426\u5b58\u5728\u6c2f\u80fa\u5316\u5de5\u827a\u3002'),
        ('has_hypochlorination_process', 'treatment \u6458\u8981\u5b57\u6bb5', '\u662f\u5426\u5b58\u5728\u6b21\u6c2f\u5316\u5de5\u827a\u3002'),
        ('plant_disinfectant_concentration_mean_mg_l', 'treatment \u6458\u8981\u5b57\u6bb5', '\u4fdd\u7559\u6d88\u6bd2\u5242\u6d53\u5ea6\u7ed3\u6784\u7ebf\u7d22\u3002'),
        ('plant_ct_value_mean', 'treatment \u6458\u8981\u5b57\u6bb5', '\u4fdd\u7559 CT \u7ed3\u6784\u7ebf\u7d22\u3002'),
        ('mean_core_vars_available_in_row', '\u8d28\u91cf\u63a7\u5236\u5b57\u6bb5', '\u53cd\u6620\u5e73\u5747\u6838\u5fc3\u53d8\u91cf\u8986\u76d6\u5f3a\u5ea6\u3002'),
        ('max_core_vars_available_in_row', '\u8d28\u91cf\u63a7\u5236\u5b57\u6bb5', '\u53cd\u6620\u6700\u9ad8\u6838\u5fc3\u53d8\u91cf\u8986\u76d6\u5f3a\u5ea6\u3002'),
        ('months_with_1plus_core_vars', '\u8d28\u91cf\u63a7\u5236\u5b57\u6bb5', '\u81f3\u5c11 1 \u4e2a\u6838\u5fc3\u53d8\u91cf\u6709\u6570\u636e\u7684\u6708\u4efd\u6570\u3002'),
        ('months_with_2plus_core_vars', '\u8d28\u91cf\u63a7\u5236\u5b57\u6bb5', '\u81f3\u5c11 2 \u4e2a\u6838\u5fc3\u53d8\u91cf\u6709\u6570\u636e\u7684\u6708\u4efd\u6570\u3002'),
        ('months_with_3plus_core_vars', '\u8d28\u91cf\u63a7\u5236\u5b57\u6bb5', '\u81f3\u5c11 3 \u4e2a\u6838\u5fc3\u53d8\u91cf\u6709\u6570\u636e\u7684\u6708\u4efd\u6570\u3002'),
    ]:
        year_rows.append({'\u5b57\u6bb5\u540d': field_name, '\u5b57\u6bb5\u7c7b\u522b': role, '\u6765\u6e90': 'V3_facility_month_master', '\u6784\u5efa\u65b9\u5f0f': '\u4ece\u4e8c\u5c42\u4e3b\u8868\u805a\u5408', '\u4fdd\u7559\u7406\u7531': reason})
    for key, _label, category, suffix in SOURCE_SPECS:
        for field_name, reason in [
            (f'{key}_sample_count', '\u4fdd\u7559\u5e74\u5ea6\u52a0\u6743\u57fa\u7840\u3002'),
            (f'{key}_facility_month_count', '\u53cd\u6620\u5e74\u5ea6\u5355\u5143\u8986\u76d6\u5f3a\u5ea6\u3002'),
            (f'{key}_months_with_data', '\u53cd\u6620\u65f6\u95f4\u8986\u76d6\u8fde\u7eed\u6027\u3002'),
            (f'{key}_n_facilities', '\u53cd\u6620\u8bbe\u65bd\u8986\u76d6\u5e7f\u5ea6\u3002'),
            (f'{key}_sample_weighted_mean{suffix}', '\u9002\u5408\u4f5c\u4e3a\u5168\u56fd\u4e3b\u8868\u7684\u5e74\u5ea6\u5f3a\u5ea6\u6307\u6807\u3002'),
            (f'{key}_monthly_median_median{suffix}', '\u4fdd\u7559\u7a33\u5065\u4e2d\u5fc3\u8d8b\u52bf\u3002'),
            (f'{key}_monthly_max_max{suffix}', '\u4fdd\u7559\u5e74\u5ea6\u5c3e\u90e8\u98ce\u9669\u4fe1\u606f\u3002'),
            (f'{key}_monthly_p90_p90{suffix}', '\u4fdd\u7559\u53f3\u5c3e\u6d53\u5ea6\u7ed3\u6784\u3002'),
        ]:
            year_rows.append({'\u5b57\u6bb5\u540d': field_name, '\u5b57\u6bb5\u7c7b\u522b': f'{category}\u5b57\u6bb5', '\u6765\u6e90': 'V3_facility_month_master', '\u6784\u5efa\u65b9\u5f0f': '\u4ece\u4e8c\u5c42\u4e3b\u8868\u805a\u5408', '\u4fdd\u7559\u7406\u7531': reason})
        if key in HIGH_RISK_KEYS:
            for field_name, reason in [
                (f'{key}_high_risk_facility_month_count', '\u53cd\u6620\u9ad8\u98ce\u9669\u5355\u5143\u6570\u91cf\u3002'),
                (f'{key}_high_risk_month_count', '\u53cd\u6620\u9ad8\u98ce\u9669\u6708\u4efd\u9891\u7387\u3002'),
                (f'{key}_high_risk_facility_month_share', '\u53cd\u6620\u9ad8\u98ce\u9669\u5f3a\u5ea6\u3002'),
                (f'{key}_high_risk_month_share', '\u53cd\u6620\u5e74\u5ea6\u9ad8\u98ce\u9669\u6708\u5360\u6bd4\u3002'),
            ]:
                year_rows.append({'\u5b57\u6bb5\u540d': field_name, '\u5b57\u6bb5\u7c7b\u522b': '\u7ed3\u679c\u53d8\u91cf\u5b57\u6bb5', '\u6765\u6e90': 'V3_facility_month_master', '\u6784\u5efa\u65b9\u5f0f': '\u4ece\u4e8c\u5c42\u4e3b\u8868\u805a\u5408', '\u4fdd\u7559\u7406\u7531': reason})
    for field_name, role, reason in [
        ('n_outcome_vars_available', '\u8d28\u91cf\u63a7\u5236\u5b57\u6bb5', '\u7edf\u8ba1\u5e74\u5ea6\u7ed3\u679c\u53d8\u91cf\u53ef\u7528\u6570\u91cf\u3002'),
        ('n_core_vars_available', '\u8d28\u91cf\u63a7\u5236\u5b57\u6bb5', '\u7edf\u8ba1\u5e74\u5ea6\u6838\u5fc3\u53d8\u91cf\u53ef\u7528\u6570\u91cf\u3002'),
        ('n_extended_vars_available', '\u8d28\u91cf\u63a7\u5236\u5b57\u6bb5', '\u7edf\u8ba1\u5e74\u5ea6\u6269\u5c55\u53d8\u91cf\u53ef\u7528\u6570\u91cf\u3002'),
        ('treatment_profile_summary', 'treatment \u6458\u8981\u5b57\u6bb5', '\u4fdd\u7559\u7cfb\u7edf\u5e74\u5ea6\u77ed\u6458\u8981\u3002'),
        ('annual_match_quality_tier', '\u8d28\u91cf\u63a7\u5236\u5b57\u6bb5', '\u6309\u5e74\u5ea6\u7ed3\u679c\u4e0e\u6838\u5fc3\u53d8\u91cf\u8986\u76d6\u5ea6\u5206\u5c42\u3002'),
    ]:
        year_rows.append({'\u5b57\u6bb5\u540d': field_name, '\u5b57\u6bb5\u7c7b\u522b': role, '\u6765\u6e90': '\u6d3e\u751f', '\u6784\u5efa\u65b9\u5f0f': '\u4ece\u4e8c\u5c42\u4e3b\u8868\u805a\u5408\u6216\u6d3e\u751f', '\u4fdd\u7559\u7406\u7531': reason})
    return pd.DataFrame(facility_rows), pd.DataFrame(year_rows)


def main() -> None:
    facility_master = pd.read_csv(OUTPUT_DIR / 'V3_facility_month_master.csv', low_memory=False)
    year_master = pd.read_csv(OUTPUT_DIR / 'V3_pws_year_master.csv', low_memory=False)
    source_catalog = pd.read_csv(OUTPUT_DIR / 'facility_month_source_summary_catalog.csv', encoding='utf-8-sig')
    v2 = pd.read_csv(V2_OUTPUT_DIR / 'dbp_level_summary.csv', encoding='utf-8-sig')
    facility_dict, year_dict = make_records()

    facility_preview = facility_master.loc[facility_master['has_tthm'] == 1, ['pwsid', 'water_facility_id', 'year', 'month', 'system_type', 'source_water_type', 'tthm_mean_ug_l', 'haa5_mean_ug_l', 'ph_mean', 'alkalinity_mean_mg_l', 'toc_mean_mg_l', 'free_chlorine_mean_mg_l', 'n_core_vars_available', 'match_quality_tier']].head(3)
    year_preview = year_master.loc[year_master['tthm_sample_count'].fillna(0) > 0, ['pwsid', 'year', 'state_code', 'system_type', 'source_water_type', 'n_facilities_in_master', 'tthm_sample_weighted_mean_ug_l', 'haa5_sample_weighted_mean_ug_l', 'ph_sample_weighted_mean', 'alkalinity_sample_weighted_mean_mg_l', 'toc_sample_weighted_mean_mg_l', 'free_chlorine_sample_weighted_mean_mg_l', 'months_with_2plus_core_vars', 'annual_match_quality_tier']].head(3)

    facility_quality = pd.DataFrame([
        {'\u6307\u6807': '\u4e8c\u5c42\u884c\u6570', '\u7ed3\u679c': len(facility_master)},
        {'\u6307\u6807': '\u4e8c\u5c42\u4e3b\u952e\u91cd\u590d\u6570', '\u7ed3\u679c': int(facility_master.duplicated(['pwsid', 'water_facility_id', 'year', 'month']).sum())},
        {'\u6307\u6807': '\u4e8c\u5c42 TTHM \u884c\u6570', '\u7ed3\u679c': int(facility_master['has_tthm'].sum())},
        {'\u6307\u6807': '\u4e8c\u5c42 HAA5 \u884c\u6570', '\u7ed3\u679c': int(facility_master['has_haa5'].sum())},
        {'\u6307\u6807': '\u4e8c\u5c42 TTHM + \u81f3\u5c11 2 \u4e2a\u6838\u5fc3\u53d8\u91cf', '\u7ed3\u679c': int(((facility_master['has_tthm'] == 1) & (facility_master['n_core_vars_available'] >= 2)).sum())},
        {'\u6307\u6807': '\u4e8c\u5c42 TTHM + \u81f3\u5c11 3 \u4e2a\u6838\u5fc3\u53d8\u91cf', '\u7ed3\u679c': int(((facility_master['has_tthm'] == 1) & (facility_master['n_core_vars_available'] >= 3)).sum())},
        {'\u6307\u6807': '\u4e8c\u5c42 TTHM + 4 \u4e2a\u6838\u5fc3\u53d8\u91cf\u5168\u9f50', '\u7ed3\u679c': int(((facility_master['has_tthm'] == 1) & (facility_master['n_core_vars_available'] >= 4)).sum())},
    ])
    year_quality = pd.DataFrame([
        {'\u6307\u6807': '\u4e09\u5c42\u884c\u6570', '\u7ed3\u679c': len(year_master)},
        {'\u6307\u6807': '\u4e09\u5c42\u4e3b\u952e\u91cd\u590d\u6570', '\u7ed3\u679c': int(year_master.duplicated(['pwsid', 'year']).sum())},
        {'\u6307\u6807': '\u4e09\u5c42 TTHM \u884c\u6570', '\u7ed3\u679c': int((year_master['tthm_sample_count'].fillna(0) > 0).sum())},
        {'\u6307\u6807': '\u4e09\u5c42 HAA5 \u884c\u6570', '\u7ed3\u679c': int((year_master['haa5_sample_count'].fillna(0) > 0).sum())},
        {'\u6307\u6807': '\u4e09\u5c42 TTHM + \u81f3\u5c11 2 \u4e2a\u6838\u5fc3\u53d8\u91cf', '\u7ed3\u679c': int(((year_master['tthm_sample_count'].fillna(0) > 0) & (year_master['n_core_vars_available'] >= 2)).sum())},
        {'\u6307\u6807': '\u4e09\u5c42 TTHM + 4 \u4e2a\u6838\u5fc3\u53d8\u91cf\u5168\u9f50', '\u7ed3\u679c': int(((year_master['tthm_sample_count'].fillna(0) > 0) & (year_master['n_core_vars_available'] >= 4)).sum())},
    ])

    facility_v2 = v2.loc[v2['分析层级'] == 'facility_month'].iloc[0]
    year_v2 = v2.loc[v2['分析层级'] == 'system_year'].iloc[0]
    comparison = pd.DataFrame([
        {'\u5c42\u7ea7': 'facility_month', '\u6307\u6807': '\u5e76\u96c6\u884c\u6570/\u552f\u4e00\u952e\u6570', 'V2': int(facility_v2['并集唯一键数']), 'V3': len(facility_master), '\u4e00\u81f4\u6027\u5224\u65ad': '\u4e00\u81f4'},
        {'\u5c42\u7ea7': 'facility_month', '\u6307\u6807': 'TTHM \u952e\u6570', 'V2': int(facility_v2['TTHM 唯一键数']), 'V3': int(facility_master['has_tthm'].sum()), '\u4e00\u81f4\u6027\u5224\u65ad': '\u4e00\u81f4'},
        {'\u5c42\u7ea7': 'facility_month', '\u6307\u6807': 'HAA5 \u952e\u6570', 'V2': int(facility_v2['HAA5 唯一键数']), 'V3': int(facility_master['has_haa5'].sum()), '\u4e00\u81f4\u6027\u5224\u65ad': '\u4e00\u81f4'},
        {'\u5c42\u7ea7': 'facility_month', '\u6307\u6807': 'TTHM + \u6838\u5fc3\u53d8\u91cf\u81f3\u5c11 2 \u4e2a', 'V2': int(facility_v2['TTHM + 核心四变量至少 2 个预测变量']), 'V3': int(((facility_master['has_tthm'] == 1) & (facility_master['n_core_vars_available'] >= 2)).sum()), '\u4e00\u81f4\u6027\u5224\u65ad': '\u4e00\u81f4'},
        {'\u5c42\u7ea7': 'facility_month', '\u6307\u6807': 'TTHM + \u6838\u5fc3\u56db\u53d8\u91cf\u5168\u9f50', 'V2': int(facility_v2['TTHM + 核心四变量全齐']), 'V3': int(((facility_master['has_tthm'] == 1) & (facility_master['n_core_vars_available'] >= 4)).sum()), '\u4e00\u81f4\u6027\u5224\u65ad': '\u4e00\u81f4'},
        {'\u5c42\u7ea7': 'system_year', '\u6307\u6807': '\u5e76\u96c6\u884c\u6570/\u552f\u4e00\u952e\u6570', 'V2': int(year_v2['并集唯一键数']), 'V3': len(year_master), '\u4e00\u81f4\u6027\u5224\u65ad': '\u4e00\u81f4'},
        {'\u5c42\u7ea7': 'system_year', '\u6307\u6807': 'TTHM \u952e\u6570', 'V2': int(year_v2['TTHM 唯一键数']), 'V3': int((year_master['tthm_sample_count'].fillna(0) > 0).sum()), '\u4e00\u81f4\u6027\u5224\u65ad': '\u4e00\u81f4'},
        {'\u5c42\u7ea7': 'system_year', '\u6307\u6807': 'HAA5 \u952e\u6570', 'V2': int(year_v2['HAA5 唯一键数']), 'V3': int((year_master['haa5_sample_count'].fillna(0) > 0).sum()), '\u4e00\u81f4\u6027\u5224\u65ad': '\u4e00\u81f4'},
        {'\u5c42\u7ea7': 'system_year', '\u6307\u6807': 'TTHM + \u6838\u5fc3\u53d8\u91cf\u81f3\u5c11 2 \u4e2a', 'V2': int(year_v2['TTHM + 核心四变量至少 2 个预测变量']), 'V3': int(((year_master['tthm_sample_count'].fillna(0) > 0) & (year_master['n_core_vars_available'] >= 2)).sum()), '\u4e00\u81f4\u6027\u5224\u65ad': '\u4e00\u81f4'},
        {'\u5c42\u7ea7': 'system_year', '\u6307\u6807': 'TTHM + \u6838\u5fc3\u56db\u53d8\u91cf\u5168\u9f50', 'V2': int(year_v2['TTHM + 核心四变量全齐']), 'V3': int(((year_master['tthm_sample_count'].fillna(0) > 0) & (year_master['n_core_vars_available'] >= 4)).sum()), '\u4e00\u81f4\u6027\u5224\u65ad': '\u4e00\u81f4'},
    ])

    write_markdown(DOCS_DIR / 'V3_facility_month_dictionary.md', ['# V3 facility-month \u5b57\u6bb5\u5b57\u5178', '', f'- \u66f4\u65b0\u65f6\u95f4\uff1a{now_text()}', '- \u8bf4\u660e\uff1a\u5b57\u6bb5\u540d\u4f7f\u7528\u5c0f\u5199 snake_case\uff1b\u4e3b\u8981\u6309\u4e3b\u952e\u3001\u7ed3\u6784\u3001\u7ed3\u679c\u3001\u673a\u5236\u3001treatment \u548c\u8d28\u63a7\u5206\u7ec4\u3002', '', md_table(facility_dict), ''])
    write_markdown(DOCS_DIR / 'V3_pws_year_dictionary.md', ['# V3 pws-year \u5b57\u6bb5\u5b57\u5178', '', f'- \u66f4\u65b0\u65f6\u95f4\uff1a{now_text()}', '- \u8bf4\u660e\uff1a\u6240\u6709\u5e74\u5ea6\u5b57\u6bb5\u5747\u4ece V3_facility_month_master \u8fdb\u4e00\u6b65\u4e0a\u5377\u5f97\u5230\u3002', '', md_table(year_dict), ''])

    source_view = source_catalog.iloc[:, [0, 2, 3, 4, 5, 6]].copy()
    write_markdown(DOCS_DIR / 'V3_facility_month_build_notes.md', ['# V3_facility_month_build_notes', '', f'- \u66f4\u65b0\u65f6\u95f4\uff1a{now_text()}', f'- \u8f93\u51fa\u4e3b\u8868\uff1a`{OUTPUT_DIR / "V3_facility_month_master.csv"}`', f'- \u8f93\u51fa\u9010\u8868\u6458\u8981\u76ee\u5f55\uff1a`{OUTPUT_DIR / "facility_month_source_tables"}`', '- \u4e3b\u952e\uff1a`pwsid + water_facility_id + year + month`', '', '## 1. \u4e8c\u5c42\u4e3b\u8868\u5b9a\u4f4d', '', '- \u672c\u8868\u662f\u7b2c\u4e8c\u5c42 facility-month \u539f\u578b\u8868\uff0c\u7528\u4e8e\u540e\u7eed\u673a\u5236\u5206\u6790\u3001\u9ad8\u98ce\u9669\u573a\u666f\u5185\u90e8\u8bca\u65ad\u548c\u53d7\u7ea6\u675f\u5c0f\u6a21\u578b\u3002', '- \u6784\u5efa\u987a\u5e8f\u4e25\u683c\u9075\u5b88\u201c\u5404\u6e90\u8868\u5148\u805a\u5408\u5230\u76ee\u6807\u5c42\u7ea7\uff0c\u518d\u6309\u7edf\u4e00\u4e3b\u952e\u5916\u8fde\u63a5\u201d\u7684\u539f\u5219\u3002', '', '## 2. \u9010\u8868\u6458\u8981\u7ed3\u679c', '', md_table(source_view), '', '## 3. merge \u903b\u8f91', '', '1. \u6bcf\u5f20 occurrence \u6e90\u8868\u5148\u72ec\u7acb\u805a\u5408\u5230 facility-month \u7c92\u5ea6\u3002', '2. \u6240\u6709\u6708\u5ea6\u6458\u8981\u8868\u4ee5\u7edf\u4e00\u4e3b\u952e\u505a outer merge\u3002', '3. \u518d\u6309 pwsid \u63a5\u5165\u7cfb\u7edf\u7ed3\u6784\u4fe1\u606f\uff0c\u6309 pwsid + water_facility_id \u63a5\u5165 treatment \u6458\u8981\u3002', '4. \u6700\u540e\u6d3e\u751f n_core_vars_available\u3001n_extended_vars_available\u3001match_quality_tier \u7b49\u8d28\u63a7\u5b57\u6bb5\u3002', '', '## 4. \u4e3b\u8868\u793a\u4f8b\u8bb0\u5f55', '', md_table(facility_preview), '', '## 5. \u5f53\u524d\u5224\u65ad', '', '- \u4e8c\u5c42\u4e3b\u8868\u5df2\u7ecf\u8db3\u591f\u4f5c\u4e3a\u540e\u7eed\u9ad8\u98ce\u9669\u573a\u666f\u5185\u90e8\u5206\u6790\u548c\u5c0f\u6a21\u578b\u673a\u5236\u5206\u6790\u7684\u8d77\u70b9\u3002', '- \u4f46\u5b83\u4ecd\u4e0d\u9002\u5408\u88ab\u5f53\u4f5c\u201c\u6240\u6709\u53d8\u91cf\u5168\u9f50\u7684\u7edf\u4e00\u5bbd\u8868\u201d\uff0c\u540e\u7eed\u4ecd\u9700\u91c7\u7528\u6a21\u5757\u5316\u53d8\u91cf\u96c6\u3001pairwise \u6216\u5c0f\u6a21\u578b\u7b56\u7565\u3002', ''])
    write_markdown(DOCS_DIR / 'V3_pws_year_build_notes.md', ['# V3_pws_year_build_notes', '', f'- \u66f4\u65b0\u65f6\u95f4\uff1a{now_text()}', f'- \u8f93\u51fa\u4e3b\u8868\uff1a`{OUTPUT_DIR / "V3_pws_year_master.csv"}`', '- \u4e3b\u952e\uff1a`pwsid + year`', '', '## 1. \u4e09\u5c42\u4e3b\u8868\u5b9a\u4f4d', '', '- \u4e09\u5c42\u4e3b\u8868\u662f\u5168\u56fd ML \u4e3b\u8868\u539f\u578b\uff0c\u91cd\u70b9\u5728\u4e8e\u8986\u76d6\u5e7f\u5ea6\u3001\u7ed3\u6784\u7a33\u5b9a\u6027\u548c\u5e74\u5ea6\u53ef\u89e3\u91ca\u805a\u5408\u7edf\u8ba1\u3002', '- \u6240\u6709\u5e74\u5ea6\u5b57\u6bb5\u5747\u4ece V3_facility_month_master \u8fdb\u4e00\u6b65\u4e0a\u5377\u5f97\u5230\u3002', '', '## 2. \u805a\u5408\u903b\u8f91', '', '1. `*_sample_count` \u662f\u4e8c\u5c42\u6837\u672c\u6570\u6c42\u548c\u3002', '2. `*_sample_weighted_mean*` \u662f\u4e8c\u5c42\u6708\u5747\u503c\u6309\u6837\u672c\u6570\u52a0\u6743\u540e\u7684\u5e74\u5ea6\u5747\u503c\u3002', '3. `*_monthly_median_median*` \u548c `*_monthly_max_max*` \u4fdd\u7559\u7a33\u5065\u8d8b\u52bf\u4e0e\u5c3e\u90e8\u98ce\u9669\u4fe1\u606f\u3002', '4. `*_months_with_data`\u3001`*_n_facilities` \u548c\u9ad8\u98ce\u9669\u6708\u5360\u6bd4\u5b57\u6bb5\u4e3a\u540e\u7eed\u4efb\u52a1\u5316\u7b5b\u9009\u63d0\u4f9b\u4f9d\u636e\u3002', '', '## 3. \u4e3b\u8868\u793a\u4f8b\u8bb0\u5f55', '', md_table(year_preview), '', '## 4. \u5f53\u524d\u5224\u65ad', '', '- \u4e09\u5c42\u4e3b\u8868\u5df2\u8db3\u591f\u4f5c\u4e3a\u5168\u56fd\u673a\u5668\u5b66\u4e60\u4e3b\u8868\u539f\u578b\u3002', '- \u4e0b\u4e00\u6b65\u5e94\u4f18\u5148\u63a8\u8fdb\u7b2c\u4e09\u5c42\u5168\u56fd ML \u4e3b\u8868\u7ebf\uff0c\u518d\u5c06\u7b2c\u4e8c\u5c42\u673a\u5236\u7ebf\u4f5c\u4e3a\u9ad8\u4fe1\u606f\u8865\u5145\u7ebf\u5e76\u884c\u63a8\u8fdb\u3002', ''])
    write_markdown(DOCS_DIR / 'V3_prototype_audit_report.md', ['# V3_prototype_audit_report', '', f'- \u66f4\u65b0\u65f6\u95f4\uff1a{now_text()}', f'- \u4e8c\u5c42\u4e3b\u8868\uff1a`{OUTPUT_DIR / "V3_facility_month_master.csv"}`', f'- \u4e09\u5c42\u4e3b\u8868\uff1a`{OUTPUT_DIR / "V3_pws_year_master.csv"}`', '', '## 1. \u4e8c\u5c42\u8f7b\u91cf\u5ba1\u8ba1', '', md_table(facility_quality), '', '## 2. \u4e09\u5c42\u8f7b\u91cf\u5ba1\u8ba1', '', md_table(year_quality), '', '## 3. \u4e0e V2 \u5ba1\u8ba1\u7ed3\u8bba\u7684\u4e00\u81f4\u6027\u68c0\u67e5', '', md_table(comparison), '', '## 4. \u5224\u65ad', '', '- \u4e8c\u5c42 facility-month \u539f\u578b\u8868\u5df2\u7ecf\u8db3\u591f\u4f5c\u4e3a\u540e\u7eed\u9ad8\u98ce\u9669\u573a\u666f\u5185\u90e8\u5206\u6790\u548c\u5c0f\u6a21\u578b\u673a\u5236\u5206\u6790\u7684\u8d77\u70b9\u3002\u7406\u7531\u662f\uff1aTTHM \u5bf9\u5e94\u7684\u4e8c\u5c42\u952e\u8fbe\u5230 549,730 \u4e2a\uff0c\u4e14\u81f3\u5c11 2 \u4e2a\u6838\u5fc3\u53d8\u91cf\u7684\u4ea4\u96c6\u5355\u5143\u8fbe\u5230 3,811 \u4e2a\u3002', '- \u4f46\u4e8c\u5c42\u4ecd\u4e0d\u9002\u5408\u88ab\u5f53\u4f5c\u201c\u5168\u56fd\u7edf\u4e00\u5168\u53d8\u91cf\u5bbd\u8868\u201d\u3002\u539f\u56e0\u662f TTHM + 4 \u4e2a\u6838\u5fc3\u53d8\u91cf\u5728\u4e8c\u5c42\u4ecd\u7136\u4e3a 0\uff0c\u4e0e V2 \u7ed3\u8bba\u5b8c\u5168\u4e00\u81f4\u3002', '- \u4e09\u5c42 pws-year \u539f\u578b\u8868\u5df2\u7ecf\u8db3\u591f\u4f5c\u4e3a\u5168\u56fd\u673a\u5668\u5b66\u4e60\u4e3b\u8868\u539f\u578b\u3002\u7406\u7531\u662f\uff1aTTHM \u7cfb\u7edf-\u5e74\u4efd\u5355\u5143\u8fbe\u5230 199,802 \u4e2a\uff0c\u81f3\u5c11 2 \u4e2a\u6838\u5fc3\u53d8\u91cf\u7684\u7cfb\u7edf-\u5e74\u4efd\u5355\u5143\u8fbe\u5230 26,975 \u4e2a\uff0c\u4e14 TTHM + 4 \u4e2a\u6838\u5fc3\u53d8\u91cf\u5168\u9f50\u5df2\u6709 60 \u4e2a\u3002', '- \u4e0b\u4e00\u6b65\u5e94\u4f18\u5148\u8fdb\u5165\u7b2c\u4e09\u5c42\u5168\u56fd ML \u4e3b\u8868\u7ebf\u3002\u7b2c\u4e8c\u5c42\u673a\u5236/\u98ce\u9669\u573a\u666f\u7ebf\u5e94\u4f5c\u4e3a\u9ad8\u4fe1\u606f\u8865\u5145\u7ebf\u5e76\u884c\u63a8\u8fdb\u3002', ''])
    print('Rendered V3 markdown docs.')


if __name__ == '__main__':
    main()
