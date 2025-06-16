import gradio as gr
from app.features import create_df_for_person
from app.model import make_prediction

def predict_bot(uid: str):
    try:
        df = create_df_for_person(uid)
        prediction, probability = make_prediction(df)
        message = (
            f"✅ Пользователь — {'бот' if prediction else 'НЕ бот'} "
            f"(вероятность: {probability:.2f})"
        )
        return message
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"

with gr.Blocks(title="VK Bot Classifier") as demo:
    gr.Markdown("## 🤖 VK Bot Classifier")
    gr.Markdown("Определяет, является ли пользователь ботом на основе его данных")

    with gr.Row():
        with gr.Column(scale=1):
            uid_input = gr.Textbox(
                label="🔗 Введите ссылку или ID пользователя VK",
                placeholder="например, id1, durov, или https://vk.com/durov",
                value=""
            )
            with gr.Row():
                submit_btn = gr.Button("🔍 Проверить")
                clear_btn = gr.Button("🧹 Очистить")

        with gr.Column(scale=1):
            result_output = gr.Textbox(
                label="📊 Результат",
                lines=2,
                max_lines=2,
                interactive=False
            )

    submit_btn.click(fn=predict_bot, inputs=uid_input, outputs=result_output)
    clear_btn.click(fn=lambda: "", outputs=result_output)

    gr.Markdown(
        """
---
**👨‍💻 Проект разработан студентами:**
 
- Гильмутдинов Ринат Рашитович  
- Рязанов Виктор Вадимович 
- Ходько Владимир Валерьевич 
- Кобелев Данила Александрович  

📂 **[Репозиторий на GitHub](https://github.com/Ryazanov-Viktor/URFU_Software_Engineering_VK_Bots)**
        """
    )

if __name__ == "__main__":
    demo.launch()



