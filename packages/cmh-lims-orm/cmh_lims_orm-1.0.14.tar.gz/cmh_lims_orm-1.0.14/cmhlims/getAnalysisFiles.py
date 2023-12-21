from cmhlims.connectToLIMS import connect_to_lims
from typing import List
import pandas as pd
from sqlalchemy import create_engine, MetaData, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, aliased, relationship

def get_analysis_files(analysis_ids: List[str]) -> pd.DataFrame:
    if len(analysis_ids) == 0:
        raise ValueError("get_analysis_files() requires at least one analysis_id")

    engine = connect_to_lims()
    metadata = MetaData()

    Base = automap_base(metadata=metadata)
    Base.prepare(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    lims_tables = ["downstream_analysis_files", "downstream_analysis_file_types", "downstream_analyses"]

    metadata.reflect(engine, only=lims_tables)

    DownstreamAnalysisFiles = Base.classes.downstream_analysis_files
    DownstreamAnalysisFileTypes = Base.classes.downstream_analysis_file_types
    DownstreamAnalyses = Base.classes.downstream_analyses

    f = aliased(DownstreamAnalysisFiles)
    t = aliased(DownstreamAnalysisFileTypes)
    a = aliased(DownstreamAnalyses)

    # Specify relationships
    DownstreamAnalysisFiles.downstream_analysis = relationship(DownstreamAnalyses, backref='analysis_files', viewonly=True, lazy='joined')
    DownstreamAnalysisFiles.file_type = relationship(DownstreamAnalysisFileTypes, backref='analysis_files', viewonly=True, lazy='joined')

    # Create a query
    query = (
        session.query(
            f.file_path.label('file_path'),
            a.id.label('analysis_id'),
            t.label.label('file_type_label'),
            t.abbrev.label('file_type_abbrev')
        )
        .join(a, a.id == f.downstream_analysis_id)
        .join(t, f.downstream_analysis_file_type_id == t.id)
        .filter(a.id.in_(analysis_ids))
    )

    # Execute the query
    result = query.all()

    # Convert result to DataFrame
    columns = ['file_path', 'analysis_id', 'file_type_label', 'file_type_abbrev']
    files_df = pd.DataFrame(result, columns=columns)

    return files_df


if __name__ == "__main__":
    output = get_analysis_files(analysis_ids = ["2287"])
    print(output)
