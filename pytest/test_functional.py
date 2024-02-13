import os
import subprocess
import tempfile


def test_main():
    # Create two temporary files
    with tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as jp_file, tempfile.NamedTemporaryFile('w+', delete=False, encoding='utf-8') as cn_file:
        # Write some data to the files
        jp_file.write(JP_INITIAL)
        cn_file.write(CN_INITIAL)

        # Make sure the data is written to disk
        jp_file.flush()
        cn_file.flush()

        # Close the files
        jp_file.close()
        cn_file.close()

        # Run the main.py script with the temporary files as parameters
        result = subprocess.run(['python', 'main.py', jp_file.name, cn_file.name], capture_output=True, text=True)

        # Check the exit code
        assert result.returncode == 0

        # Check the output
        # expected_stdout = "\n".join([
        #     "Realignment process completed successfully.",
        #     "Proceeding to overwrite the original files with the processed content.",
        #     "Files have been processed and overwritten."
        # ])
        # assert expected_stdout in result.stdout

        # Reopen the files in read mode
        with open(jp_file.name, 'r', encoding='utf-8') as jp_file, open(cn_file.name, 'r', encoding='utf-8') as cn_file:
            # Read the files and check their contents
            assert jp_file.read() == JP_FINAL
            assert cn_file.read() == CN_FINAL

    # Delete the temporary files
    os.remove(jp_file.name)
    os.remove(cn_file.name)


JP_INITIAL = '''　メッセージアプリから、着信を知らせる通知が光り、那月はベッドで寝転がったまま、スマホに手を伸ばした。

「あれ。雛子からだ」

　那月の幼馴染である彼女からの着信だった。

　スマホのディスプレイをタップし、那月は電話に応じる。

「もしもし。どうしたの、雛子」

　ベッドに寝そべったまま尋ねれば、聞きなれた雛子の声が聴こえる。

「那月、あけおめ～！　今って、実家？　下宿？」

　新年を迎えて、そこそこの日付が経つが、かまうことなく雛子が新年の挨拶を交わす。

　年明けの瞬間に、メッセージを送りあったことを、ふと思い出し、那月は一人、笑って、口を開く。

「もう、大学の方の家に戻って来てるよ」

「そっか、良かった～。あのね、私も今、下宿なんだけど……、今から、私の家に来れない？」

「えっ」

　突然の提案に、那月は、戸惑いの声をあげる。

　残り少ない冬休み。お互いの家に遊びに行くことなど、これまでは珍しい話ではなかったのだが、今となっては、どきりとしてしまう。

　だって、私たち、これまでとは、立場が違うわけだし。

　そんな那月の様子もかまわず、雛子は言葉を続ける。

「実は、ちょっと、私、今こまってて……。那月に助けてもらえたらなあって」'''

JP_FINAL = '''メッセージアプリから、着信を知らせる通知が光り、那月はベッドで寝転がったまま、スマホに手を伸ばした。
「あれ。雛子からだ」
那月の幼馴染である彼女からの着信だった。
スマホのディスプレイをタップし、那月は電話に応じる。
「もしもし。どうしたの、雛子」
ベッドに寝そべったまま尋ねれば、聞きなれた雛子の声が聴こえる。
「那月、あけおめ～！　今って、実家？　下宿？」
新年を迎えて、そこそこの日付が経つが、かまうことなく雛子が新年の挨拶を交わす。
年明けの瞬間に、メッセージを送りあったことを、ふと思い出し、那月は一人、笑って、口を開く。
「もう、大学の方の家に戻って来てるよ」
「そっか、良かった～。あのね、私も今、下宿なんだけど……、今から、私の家に来れない？」
「えっ」
突然の提案に、那月は、戸惑いの声をあげる。
残り少ない冬休み。お互いの家に遊びに行くことなど、これまでは珍しい話ではなかったのだが、今となっては、どきりとしてしまう。
だって、私たち、これまでとは、立場が違うわけだし。
そんな那月の様子もかまわず、雛子は言葉を続ける。
「実は、ちょっと、私、今こまってて……。那月に助けてもらえたらなあって」'''

CN_INITIAL = '''从通讯软件传来收到消息的提示音，那月转过身来将手伸向了自己的手机。
「啊嘞，雏子。」

收到的这条消息来自那月的青梅竹马，雏子。
手机点击屏幕，那月向对方回了个电话。

「莫西莫西？怎么啦雏子」

侧躺在床上，电话那头传来了熟悉的声音。

「那月，新年快乐～现在在...老家？下宿町？」

又迎来了新的一年，虽然两人已经相处已久，但雏子也是毫无保留地送来了新年祝福。
想到对方在跨年的一瞬间向自己发送信息的样子，那月不禁莞尔一笑。

「真是的，回到大学这边的房子了哦。」

「这样啊，太好啦~那个，现在我在下宿哦....现在，来我家一趟？」

「诶？」

对方突然而来的提案使得那月发出疑惑的声音。
寒假已经临近结尾。虽然一直以来去对方家玩这样的事情已经不在少数，但是仍然让那月吃了一惊。毕竟，两人已经走上不同的生活了。

然而并没有理会那月的迟疑，雏子继续说着。
「实际上...那个...我...现在稍微有点那个....有点事想那月帮帮我...」'''

CN_FINAL = '''从通讯软件传来收到消息的提示音，那月转过身来将手伸向了自己的手机。
「啊嘞，雏子。」
收到的这条消息来自那月的青梅竹马，雏子。
手机点击屏幕，那月向对方回了个电话。
「莫西莫西？怎么啦雏子」
侧躺在床上，电话那头传来了熟悉的声音。
「那月，新年快乐～现在在...老家？下宿町？」
又迎来了新的一年，虽然两人已经相处已久，但雏子也是毫无保留地送来了新年祝福。
想到对方在跨年的一瞬间向自己发送信息的样子，那月不禁莞尔一笑。
「真是的，回到大学这边的房子了哦。」
「这样啊，太好啦~那个，现在我在下宿哦....现在，来我家一趟？」
「诶？」
对方突然而来的提案使得那月发出疑惑的声音。
寒假已经临近结尾。虽然一直以来去对方家玩这样的事情已经不在少数，但是仍然让那月吃了一惊。毕竟，两人已经走上不同的生活了。
然而并没有理会那月的迟疑，雏子继续说着。
;
「实际上...那个...我...现在稍微有点那个....有点事想那月帮帮我...」'''
