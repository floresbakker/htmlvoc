#!/usr/bin/env python3
"""Validate generated HTML table RDF against the baseline regression data."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pyshacl
from rdflib import Dataset


REGRESSION_DIR = Path(__file__).resolve().parent
DEFAULT_BASELINE = REGRESSION_DIR / "html_table_regression_baseline.trig"
DEFAULT_SHAPES = REGRESSION_DIR / "html_table_regression_shapes.trig"


def main() -> int:
    logging.getLogger("rdflib.term").setLevel(logging.CRITICAL)

    args = parse_args()

    data_graph = Dataset(default_union=True)
    data_graph.parse(args.baseline_data, format=rdf_format(args.baseline_data))
    for path in args.new_data:
        data_graph.parse(path, format=rdf_format(path))

    conforms, report_graph, report_text = pyshacl.validate(
        data_graph=data_graph,
        shacl_graph=str(args.shapes),
        shacl_graph_format=rdf_format(args.shapes),
        inference=None,
        advanced=True,
    )

    if args.report_graph:
        report_graph.serialize(
            destination=args.report_graph,
            format=rdf_format(args.report_graph),
        )

    print(report_text)
    return 0 if conforms else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Load baseline RDF, load newly generated RDF, and validate the "
            "HTML table regression SHACL shapes."
        )
    )
    parser.add_argument(
        "--baseline-data",
        type=Path,
        default=DEFAULT_BASELINE,
        help="Baseline RDF with regression scenarios and expected HTML fragments.",
    )
    parser.add_argument(
        "--new-data",
        type=Path,
        nargs="+",
        required=True,
        help="Newly generated RDF file(s) to compare with the baseline data.",
    )
    parser.add_argument(
        "--shapes",
        type=Path,
        default=DEFAULT_SHAPES,
        help="SHACL shape file used for the regression comparison.",
    )
    parser.add_argument(
        "--report-graph",
        type=Path,
        help="Optional path for the SHACL validation report graph.",
    )
    return parser.parse_args()


def rdf_format(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".trig", ".trigs"}:
        return "trig"
    if suffix in {".ttl", ".turtle"}:
        return "turtle"
    if suffix in {".nt", ".ntriples"}:
        return "nt"
    if suffix in {".jsonld", ".json"}:
        return "json-ld"
    return "turtle"


if __name__ == "__main__":
    sys.exit(main())
