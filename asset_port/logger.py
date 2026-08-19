import unreal
from pathlib import Path
from asset_port.models import PipelineReport
from asset_port.localization import localize_message, tr



def log_pipeline_report(report: PipelineReport, selected_path :str, dry_run = False):
    if dry_run:
        unreal.log("===================================================")
        unreal.log(f"{tr('report.scanned')}: {report.total_scanned}")
        unreal.log(f"{tr('report.mi_created')}: {report.mis_created}")
        unreal.log("===================================================")
        if report.warnings:
            for warning in report.warnings:
                unreal.log_warning(f"{tr('report.warning')}: {localize_message(warning)}")
        
        if report.errors:
            for error in report.errors:
                unreal.log_error(f"{tr('report.error')}: {localize_message(error)}")
    else:
        unreal.log("===================================================")
        unreal.log(f"{tr('report.scanned')}: {report.total_scanned} | {tr('report.imported')}: {report.asset_import}")
        unreal.log(f"{tr('report.mi_created')}: {report.mis_created} | {tr('report.mi_linked')}: {report.mis_linked}")
        unreal.log("===================================================")
        if report.warnings:
            for warning in report.warnings:
                unreal.log_warning(f"{tr('report.warning')}: {localize_message(warning)}")
        
        if report.errors:
            for error in report.errors:
                unreal.log_error(f"{tr('report.error')}: {localize_message(error)}")
            
    if dry_run:
        preview_file_path = Path(selected_path) / "assetport_preview_report.txt"
        with open(preview_file_path, "w") as f:
            f.write("AssetPort Preview Report\n")
            f.write(f"{tr('report.scanned')}: {report.total_scanned}\n")
            
            if report.warnings:
                for warning in report.warnings:
                    f.write(f"{tr('report.warning')}: {localize_message(warning)}\n")
                    
            if report.errors:
                for error in report.errors:
                    f.write(f"{tr('report.error')}: {localize_message(error)}\n")
        
    else:        
        report_file_path = Path(selected_path) /  "assetport_report.txt"
        with open(report_file_path, "w") as f:
            f.write("AssetPort Import report\n")
            f.write(f"{tr('report.scanned')}: {report.total_scanned}\n")
            f.write(f"{tr('report.imported')}: {report.asset_import}\n")
        
            if report.warnings:
                for warning in report.warnings:
                    f.write(f"{tr('report.warning')}: {localize_message(warning)}\n")
            
            if report.errors:
                for error in report.errors:
                    f.write(f"{tr('report.error')}: {localize_message(error)}\n")
        
        
