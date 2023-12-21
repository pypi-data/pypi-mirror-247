from cmhlims.connectToLIMS import connect_to_lims
import pandas as pd
from sqlalchemy import create_engine, MetaData, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, aliased, relationship

def get_analysis(sample_names: list, reference_genome: str) -> pd.DataFrame:
    if not reference_genome:
        raise ValueError("get_analyses() supports only a single reference genome")

    if not sample_names:
        raise ValueError("get_analyses() requires at least one sample name")

    engine = connect_to_lims()
    metadata = MetaData()

    Base = automap_base(metadata=metadata)
    Base.prepare(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    lims_tables = ["samples", "downstream_analyses", "downstream_analysis_types", "sequence_types", "reference_genomes"]

    metadata.reflect(engine, only=lims_tables)

    Sample = Base.classes.samples
    DownstreamAnalyses = Base.classes.downstream_analyses
    DownsteamanalysisTypes = Base.classes.downstream_analysis_types
    SequenceTypes = Base.classes.sequence_types
    ReferenceGenomes = Base.classes.reference_genomes

    s = aliased(Sample)
    a = aliased(DownstreamAnalyses)
    t = aliased(DownsteamanalysisTypes)
    q = aliased(SequenceTypes)
    r = aliased(ReferenceGenomes)

    # Specify relationships
    Sample.downstream_analyses = relationship(DownstreamAnalyses, backref='sample', viewonly=True, lazy='joined')

    filter_conditions = [
        r.label == reference_genome,
        s.label.in_(sample_names)
    ]

    # Create a query
    query = (
        session.query(
            s.label.label('sample_name'),
            a.id.label('analysis_id'),
            a.label.label('analysis_name'),
            a.base_dir.label('analysis_dir'),
            a.analysis_date.label('analysis_date'),
            q.label.label('sequence_type'),
            t.label.label('analysis_type'),
            r.label.label('reference_genome'),
        )
        .join(a, s.downstream_analyses)
        .join(q, a.sequence_types)
        .join(r, a.reference_genomes)
        .join(t, a.downstream_analysis_types)
        .filter(and_(*filter_conditions))
    )

    # Execute the query
    result = query.all()

    # Convert result to DataFrame
    columns = ['sample_name', 'analysis_id', 'analysis_name', 'analysis_dir', 'analysis_date', 'sequence_type', 'analysis_type', 'reference_genome']
    analyses_df = pd.DataFrame(result, columns=columns)

    return analyses_df


if __name__ == "__main__":
    print(get_analysis( ["cmh000514"], "GRCh38"))
