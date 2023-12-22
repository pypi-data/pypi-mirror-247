# entrypoint.py

from .vcf_simple_annotator import annotate_vcf
from .version import __version__
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="GeneBe client, v" + __version__ + " :: https://genebe.net",
    )
    parser.add_argument("input_vcf_path", help="Path to the input VCF file")
    parser.add_argument("output_vcf_path", help="Path to the output VCF file")
    parser.add_argument(
        "--genome", default="hg38", help="Genome version (default: hg38)"
    )
    parser.add_argument(
        "--use_ensembl",
        action="store_true",
        help="Use Ensembl data for annotation",
        default=True,
    )
    parser.add_argument(
        "--use_refseq",
        action="store_true",
        help="Use RefSeq data for annotation",
        default=True,
    )
    parser.add_argument(
        "--flatten_consequences",
        action="store_true",
        help="Flatten consequences in the output",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=500,
        help="Batch size for API requests (default: 500)",
    )
    parser.add_argument("--username", help="Username for API authentication")
    parser.add_argument("--api_key", help="API key for authentication")
    parser.add_argument(
        "--use_netrc", action="store_true", help="Use .netrc file for authentication"
    )
    parser.add_argument(
        "--endpoint_url",
        default="https://api.genebe.net/cloud/api-public/v1/variants",
        help="API endpoint URL (default: https://api.genebe.net/cloud/api-public/v1/variants)",
    )

    args = parser.parse_args()

    # Call the annotate_vcf function with the provided arguments
    annotate_vcf(
        input_vcf_path=args.input_vcf_path,
        output_vcf_path=args.output_vcf_path,
        genome=args.genome,
        use_ensembl=args.use_ensembl,
        use_refseq=args.use_refseq,
        flatten_consequences=args.flatten_consequences,
        batch_size=args.batch_size,
        username=args.username,
        api_key=args.api_key,
        use_netrc=args.use_netrc,
        endpoint_url=args.endpoint_url,
    )


if __name__ == "__main__":
    main()
