import csv

def main():
	couples = list(csv.DictReader(open('out.csv')))

if __name__ == '__main__':
	main()
