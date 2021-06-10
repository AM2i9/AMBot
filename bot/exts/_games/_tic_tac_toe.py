import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        DiscordComponents(self.bot)

    def checkForWin(board):
        win = (
            board[0] == board[1] and board[1] == board[2]
            or board[3] == board[4] and board[4] == board[5]
            or board[6] == board[7] and board[7] == board[8]
            or board[0] == board[4] and board[4] == board[8]
            or board[2] == board[4] and board[4] == board[6]
        )
        if not any(i.isdigit() for i in board) and not win:
            return 2
        else:
            return win
    
    def getButtonStyle(value):
            if value == 'X':
                return ButtonStyle.blue
            elif value == 'O':
                return ButtonStyle.red
            else:
                return ButtonStyle.gray
    
    async def game(self, ctx, user):
        components = [
            [Button(style=ButtonStyle.gray,label=str(ia+i)) for ia in range(3)] for i in range(1,9,3)
        ]
        gamemsg = await ctx.send(f'{user.mention}, {ctx.author.name} has challenged thee to tic-tac-toe! You go first.', components=components)

        turn = 'X'
        players = {
            'X': user,
            'O': ctx.author
        }

        def checkEvent(event):
            component = event.component
            if type(component) is not dict:
                component = event.component.to_dict()
            return (
                (component['label'] != 'X' and component['label'] != 'O')
                and event.message.id == gamemsg.id
                and (event.user == players[turn])
            )

        while True:
            boardClick = await self.bot.wait_for('button_click', check=checkEvent)
            moveComponent = boardClick.component
            if type(moveComponent) is not dict:
                moveComponent = boardClick.component.to_dict()
            board = [button.label for button in boardClick.message.components]
            squareClicked = board.index(moveComponent["label"])
            board[squareClicked] = turn

            gameWon = self.checkForWin(board)

            components = [[Button(style=self.getButtonStyle(board[i+ia-1]),label=board[i+ia-1],disabled=bool(gameWon)) for ia in range(3)] for i in range(1,9,3)]

            if gameWon:
                if gameWon == 2:
                    await boardClick.respond(type=7,content=f'Game Over! It is a tie!', components = components)
                else:
                    await boardClick.respond(type=7,content=f'Game Over! {players[turn].mention} has won!', components = components)
                break

            if (turn == 'X'):
                turn = 'O'
            else:
                turn = "X"
            
            await boardClick.respond(type=7,content=f"It is {players[turn].mention}'s turn.", components = components)

    @commands.command(aliases=['ttt','tic-tac-toe'])
    async def tictactoe(self, ctx, user: discord.Member = None):

        while not user:
            await ctx.send(f"{ctx.author.mention} please mention who you would like to play against.")
            reply = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
            user = reply.mentions[0]

        if ctx.author == user:
            await ctx.send(f"{ctx.author.mention} You can't challenge yourself!")
            return
        if user.bot:
            await ctx.send(f"{ctx.author.mention} I don't think bot's know how to play tic-tac-toe...")
            return
        
        await self.game(ctx, user)