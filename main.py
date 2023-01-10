from bioseq.fqanalyze.readdata import ReadLength,GetJsonData

def argparserLocal():
    from argparse import ArgumentParser
    '''Argument parser for the commands'''
    parser = ArgumentParser(prog='myseq', description='Work with sequence')
    subparsers = parser.add_subparsers(
        title='commands', description='Please choose command below:',
        dest='command'
    )
    subparsers.required = True
    cgc_command = subparsers.add_parser('ReadLength', help='Extract data from gz file')
    cgc_command.add_argument("-r", "--readgz", type=str, default=None, dest='readgz',
                             help="Provide your .gz file")    
    cgc_command = subparsers.add_parser('GetJsonData', help='Load data from json file')
    cgc_command.add_argument("-r", "--jsonname", type=str, default=None, dest='jsonname',
                             help="Provide results.json file")
    cgc_command.add_argument("-q", "--filterQ",type=int, dest='filterQ',  default=None,
                             help="filter Qscore option")
    cgc_command.add_argument("-l", "--filterL",type=int, dest='filterL',   default=None,
                             help="filter Length option")
    return parser
    
def main():
    parser = argparserLocal()
    args = parser.parse_args()  
    if args.command == 'ReadLength':
        if args.readgz == None:
            exit(parser.parse_args(['ReadLength','-h']))
        readgz = args.readgz
        print(ReadLength(readgz))        
    elif args.command == 'GetJsonData':
        filterQ = 0
        filterL = 0
        print(args.filterQ)
        print(args.filterL)
        if args.jsonname == None:
            exit(parser.parse_args(['GetJsonData','-h']))        
        if args.filterQ != None:
            filterQ = args.filterQ            
        if args.filterL != None:            
            filterL =  args.filterL
        jsonname = args.jsonname        
        print("filterQ:",filterQ)
        print("filterL:",filterL)
        GetJsonData(jsonname,filterQ,filterL)   
        print("Loading Completed!")  
    



if __name__ == "__main__":   
       main()



