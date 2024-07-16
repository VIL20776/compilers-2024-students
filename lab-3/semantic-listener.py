import sys
from antlr4 import *
from gen.ConfRoomSchedulerLexer import ConfRoomSchedulerLexer
from gen.ConfRoomSchedulerParser import ConfRoomSchedulerParser
from gen.ConfRoomSchedulerListener import ConfRoomSchedulerListener

from datetime import datetime

class ConfRoomSchedulerSemanticChecker(ConfRoomSchedulerListener):
    def enterReserveStat(self, ctx):
        tokens = ctx.reserve()
        # Aqui debe colocar su codigo para validar que 
        # se cumpla con el requerimiento solicitado
        # Puede quitar el pass despues
        startTime = datetime.strptime(tokens.getChild(5).getText(), '%H:%M')
        finishTime = datetime.strptime(tokens.getChild(7).getText(), '%H:%M')
        if startTime >= finishTime:
            raise ValueError("Start time must be less than finish time")

def main():
    input_stream = FileStream(sys.argv[1])
    lexer = ConfRoomSchedulerLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ConfRoomSchedulerParser(stream)
    tree = parser.prog()
    
    semantic_checker = ConfRoomSchedulerSemanticChecker()
    walker = ParseTreeWalker()
    walker.walk(semantic_checker, tree)

if __name__ == '__main__':
    main()