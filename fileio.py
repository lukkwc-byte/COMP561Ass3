def readFile(input_file):
	Filelist=[]
	with open(input_file) as file:
		Filelist=file.read().splitlines()
	return Filelist

def writeFile(lis, output_file):
        Feed=open(output_file, "w")
        for i in range(len(lis)):
                Feed.write(lis[i]+"\n")

def readFileNS(input_file):
        Filelist=[]
        with open(input_file) as file:
                Filelist=file.read()
        return Filelist
