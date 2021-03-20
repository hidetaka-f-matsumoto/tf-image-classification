import argparse
import pandas as pd
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input history file path')
    parser.add_argument('-o', '--output', help='Output image path')
    return parser.parse_args()

def save_graph(df, out_path):
    df.iloc[:,1:].plot()
    plt.savefig(out_path)

if __name__ == '__main__':
    args = parse_args()
    df = pd.read_csv(args.input)
    save_graph(df, args.output)
