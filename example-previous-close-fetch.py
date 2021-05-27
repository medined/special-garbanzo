#!/usr/bin/env python

import specialgarbanzo.previousclosefetcher as pcf


def main():
    previous_close = pcf.fetch('NNDM')
    print(previous_close)


if __name__ == '__main__':
    main()
