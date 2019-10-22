import os
import argparse
import pandas as pd 
import numpy as np 
import apache_beam as beam 
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.textio import ReadFromText, WriteToText

root_dir = os.path.dirname(os.path.abspath(os.getcwd()))

class Split(beam.DoFn):
    def process(self, element):
        item_id, item_price, category_1, category_2, category_3, product_type = element.split(",")
        return [{
            "item_id": int(item_id),
            "item_price": float(item_price),
            "category_1": int(category_1),
            "category_2": int(category_2),
            "category_3": int(category_3),
            "product_type": int(product_type)
        }]

class CollectOpen(beam.DoFn):
    def process(self, element):
        """
        return a list of tuples containing Date and Open value
        """
        
        # first parameter of the tuple is fixed since we want to calculate the mean over the whole dataset, 
        # but you can make it dynamic to perform the next transform only on a sub-set defined by that key.
        result = [(element["category_1"], element["item_price"])]  
        
        return result


def main(source_path, destination_path, args):
    """
    defining the whole pipeline
    """
    p = beam.Pipeline(argv = args)

    values = (
        p | "ReadCSV" >> ReadFromText(source_path, skip_header_lines = True)
          | beam.ParDo(Split())
    )

    mean_item_id = (
        values | beam.ParDo(CollectOpen()) |
        "Grouping Keys Open" >> beam.GroupByKey() |
        "Calculating Mean for item price" >> beam.CombineValues(
            beam.combiners.MeanCombineFn()
        )
    )

    output = (
        mean_item_id | "WriteCSV" >> WriteToText(destination_path, file_name_suffix = ".csv")
    )

    p.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = __doc__,
        formatter_class = argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("source_path", 
    help = ("path from where file is to be read")
    )

    parser.add_argument("destination_path", 
    help = ("path to where file is to be written")
    )

    args, pipeline_args = parser.parse_known_args()

    main(args.source_path, args.destination_path, args = pipeline_args)