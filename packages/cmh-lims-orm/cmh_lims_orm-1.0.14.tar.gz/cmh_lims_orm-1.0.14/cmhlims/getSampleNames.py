from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from cmhlims.connectToLIMS import connect_to_lims
from sqlalchemy.orm import Session, sessionmaker
from typing import List

def get_sample_names() -> List[str]:
    engine = connect_to_lims()
    metadata = MetaData()

    Base = automap_base(metadata=metadata)
    Base.prepare(engine)  # Remove autoload_with here
    Session = sessionmaker(bind=engine)
    session = Session()
    lims_tables = ["samples"]
    try:
        metadata.reflect(engine, only=lims_tables)
        Sample = Base.classes.samples
        samples_query = session.query(Sample.label).all()
        # Extract sample names from the result set
        result = [result[0] for result in samples_query]
    finally:
        session.close()
    return result


if __name__ == "__main__":
    output = get_sample_names()
    print(output)
