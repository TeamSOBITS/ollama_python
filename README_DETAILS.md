## 詳細
### メッセージ型について
    Actionlib通信にて呼び出すメッセージの構成は以下のようになっています．
    ```sh
        # Goal
        string request        # リクエストメッセージ
        string room_name      # 部屋名指定
        bool is_service       # Feedbackを送るかどうか
        ---
        # Result
        string result         # 返答メッセージ
        float64 elapsed_time  # 返答まで何秒かかったか
        ---
        # Feedback
        string wip_result     # 途中経過のメッセージ
        bool end_flag         # 途中経過の送信がが終了したかどうか
    ```


### room_nameとは
    room_nameとは会話のストックを割り当てるラベルです．\
    例えばChat GPTでは各会話ごとに部屋を切り替えられると思います．\
    例としては以下のような状態です．
    ```sh
        # 部屋A
        USER : SOBITSについて教えてください
        GPT : 私は大規模言語モデルであるため，特定のワードについての知識はありません．
        USER : そうでしたか．SOBITSとは創価大学の崔研究室と萩原研究室の学生で構成されたチームです
        GPT : そうなのですね！2つの研究室の合同チームとは素晴らしいですね！
    
        # 部屋B
        USER : 数学についての質問に答えてください
        GPT : もちろんです。どのような数学の質問がありますか？
        USER : 0で割ることはなぜいけないのですか？
        GPT : 0で割るという操作は数学的に定義されていないため、意味がありません．
    ```
    このような2つの部屋A,Bがあったとします．\
    この2部屋でユーザから「SOBITSとはどのようなものですか？」と質問すれば当然部屋AではGPTが答えることができます．\
    以下回答例です．
    ```sh
        # 部屋A
        USER : SOBITSとはどのようなものですか？
        GPT : SOBITSは先程あなたに教えてもらいました．崔研究室と萩原研究室の合同チームでしたね．なにか間違いがありましたか？
    
        # 部屋B
        USER : SOBITSとはどのようなものですか？
        GPT : SOBITSについて私は知識を持ち合わせていません．数学の質問でしたらお答えすることができるかもしれません．
    ```
    このパッケージでのroom_nameはこの部屋Aや部屋Bに当てはまります．\
    room_nameはいくつでも作ることができ，Serverのlaunchを切らない限りは過去に指定したことのある部屋名を指定すればその部屋での会話の続きができます．\    



### 事前プロンプトを定義
    上でroom_nameを指定したように，事前に会話をしたように，履歴を定義しておくことができます．\
    基本的に，[/ollama/prompt/base_prompt.yaml](/prompt/base_prompt.yaml)に定義できます．
    中は一例ですが，以下のように定義しました．
    ```sh
        # 事前に会話を定義しておくことができるyamlファイル
        sobit_mini:                                             # sobit_miniという部屋では．．．
        - {user     : "My name is SOBIT MINI."}             # 「私の名前はSOBIT MINIです」とUser側から言ったら，，，  
        - {assistant: "Nice to meet you SOBIT MINI!"}       # 「よろしくね，SOBIT MINIさん」と言っている会話を予め定義しているので
                                                        # sobit_miniという部屋を指定すればこの続きから会話できます

        team_introduce:               # team_introduceという別の部屋も準備している
        - {user     : "Our team name is SOBITS."}
        - {assistant: "I love it! SOBITS sounds like a unique and fun team name."}
        - {user     : "SOBITS consists of about 30 people."}
        - {assistant: "A team of 30 people! That's impressive!"}
    ```
    sobit_miniというroom_nameではUserの名前がSOBIT MINIとしてシステムが認識した状態で会話を進めることができます．\
    また別の部屋として，team_introduceというroom_nameでは，チームSOBITSについての説明をしており，チーム名とチームの人数をシステムは知っている状態になっています．\
    これらを踏まえて，部屋や事前プロンプトを用いた簡単な操作方法について説明します．
    1. ActionServerを立ち上げる
    ```sh
    $ roslaunch ollama_python ollama.launch
    ```
    ※モデルの指定などは忘れないでください\
    2. クライアントを実行します
    ```sh
    $ rosrun ollama_python ollama_action_client.py
    # or
    $ rosrun ollama_python ollama_service_client.py
    ```
    そこでroom_nameをdefaultにして，requestに「Do you know my name?」と打ってみてください．\
    defaultという部屋は事前プロンプトにもなく今定義した部屋なので，返答は「わかりません」になったと思います．\
    ここでもう一度クライアントを実行してください．\
    今度はroom_nameをsobit_miniにして，同様にrequestを「Do you know my name?」としてみてください．\
    すると「あなたの名前はSOBIT MINIですね」という趣旨の返答が得られたと思います．\
    これは会話履歴を部屋ごとに蓄積させているので，部屋名の指定さえすれば，何度でも事前プロンプトや会話の続きから，使うことができます．
