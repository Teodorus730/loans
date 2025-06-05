import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils import *
from models import Models


# Основное окно приложения
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ кредитных данных")
        self.root.geometry("1000x800")
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.text_reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_reports_frame, text="Текстовые отчеты")
        self.setup_text_reports()
        
        self.plots_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.plots_frame, text="Графики")
        self.setup_plots()
        
        self.models_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.models_frame, text="Модели")
        self.setup_models()
        
        self.current_report = None
        
        self.models = Models()

    # Настройка вкладки текстовых отчетов
    def setup_text_reports(self):
        # Отчет 1
        frame1 = ttk.LabelFrame(self.text_reports_frame, text="Фильтрация клиентов по доходу и возрасту")
        frame1.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame1, text="Мин доход:").grid(row=0, column=0, padx=5, pady=5)
        self.income_min = ttk.Entry(frame1)
        self.income_min.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame1, text="Макс доход:").grid(row=0, column=2, padx=5, pady=5)
        self.income_max = ttk.Entry(frame1)
        self.income_max.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame1, text="Макс возраст:").grid(row=0, column=4, padx=5, pady=5)
        self.age_max = ttk.Entry(frame1)
        self.age_max.grid(row=0, column=5, padx=5, pady=5)
        
        self.rep1 = tk.BooleanVar()
        ttk.Checkbutton(frame1, text="Только отчет", variable=self.rep1).grid(
            row=0, column=6, padx=5, pady=5)
        
        ttk.Button(frame1, text="Выполнить", command=self.run_report1).grid(
            row=0, column=7, padx=5, pady=5)
        
        # Отчет 2
        frame2 = ttk.LabelFrame(self.text_reports_frame, text="Цели кредита по уровню образования")
        frame2.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame2, text="Уровень образования:").grid(row=0, column=0, padx=5, pady=5)
        self.edu_combo = ttk.Combobox(frame2, values=list(df['person_education'].unique()))
        self.edu_combo.grid(row=0, column=1, padx=5, pady=5)
        self.edu_combo.current(0)
        
        self.rep2 = tk.BooleanVar()
        ttk.Checkbutton(frame2, text="Только отчет", variable=self.rep2).grid(
            row=0, column=2, padx=5, pady=5)
        
        ttk.Button(frame2, text="Выполнить", command=self.run_report2).grid(
            row=0, column=3, padx=5, pady=5)
        
        # Отчет 3
        frame3 = ttk.LabelFrame(self.text_reports_frame, text="Кредиты по процентной ставке")
        frame3.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame3, text="Минимальная ставка (%):").grid(row=0, column=0, padx=5, pady=5)
        self.rate_min = ttk.Entry(frame3)
        self.rate_min.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame3, text="Максимальная ставка (%):").grid(row=0, column=2, padx=5, pady=5)
        self.rate_max = ttk.Entry(frame3)
        self.rate_max.grid(row=0, column=3, padx=5, pady=5)
        
        self.rep3 = tk.BooleanVar()
        ttk.Checkbutton(frame3, text="Только отчет", variable=self.rep3).grid(
            row=0, column=4, padx=5, pady=5)
        
        ttk.Button(frame3, text="Выполнить", command=self.run_report3).grid(
            row=0, column=5, padx=5, pady=5)
        
        # Отчет 4
        frame4 = ttk.LabelFrame(self.text_reports_frame, text="Сводная таблица")
        frame4.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(frame4, text="Показать сводную таблицу", command=self.run_report4).pack(
            padx=5, pady=5)
        

        self.result_frame = ttk.LabelFrame(self.text_reports_frame, text="Результаты")
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.result_text = tk.Text(self.result_frame, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.result_text, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)

    # Настройка вкладки графиков
    def setup_plots(self):
        frame_type = ttk.Frame(self.plots_frame)
        frame_type.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(frame_type, text="Тип графика:").pack(side=tk.LEFT, padx=5)
        
        self.plot_type = ttk.Combobox(frame_type, values=[
            "Распределение категориальных фичей",
            "Распределение числовых фичей",
            "Распределение числовых фичей по таргету",
            "Boxplot по таргету",
            "Распределение категориальных фичей по TARGET",
            "Зависимость между двумя числовыми фичами",
            "Тепловая карта корреляций"
        ])
        self.plot_type.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.plot_type.current(0)
        self.plot_type.bind("<<ComboboxSelected>>", self.update_plot_options)
        
        # Параметры графиков
        self.params_frame = ttk.Frame(self.plots_frame)
        self.params_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Обновляем параметры для первого типа графика
        self.update_plot_options()

    # Обновление параметров в зависимости от типа графика
    def update_plot_options(self, event=None):
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        plot_type = self.plot_type.get()
        
        if plot_type == "Распределение категориальных фичей":
            ttk.Label(self.params_frame, text="Категориальная переменная:").pack(side=tk.LEFT, padx=5)
            
            self.cat_var = ttk.Combobox(self.params_frame, 
                                      values=list(df.select_dtypes(include=[object]).columns))
            self.cat_var.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            self.cat_var.current(0)
            
        elif plot_type in ["Распределение числовых фичей", 
                          "Распределение числовых фичей по таргету"]:
            ttk.Label(self.params_frame, text="Числовая переменная:").pack(side=tk.LEFT, padx=5)
            
            self.num_var1 = ttk.Combobox(self.params_frame, 
                                        values=list(df.select_dtypes(include=np.number).columns))
            self.num_var1.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            self.num_var1.current(0)
            
        elif plot_type == "Boxplot по таргету":
            ttk.Label(self.params_frame, text="Числовая переменная:").pack(side=tk.LEFT, padx=5)
            
            self.num_var2 = ttk.Combobox(self.params_frame, 
                                        values=list(df.select_dtypes(include=np.number).columns))
            self.num_var2.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            self.num_var2.current(0)
            
            self.show_outliers = tk.BooleanVar(value=True)
            ttk.Checkbutton(self.params_frame, text="Показать выбросы", 
                           variable=self.show_outliers).pack(side=tk.LEFT, padx=10)
            
        elif plot_type == "Распределение категориальных фичей по TARGET":
            ttk.Label(self.params_frame, text="Категориальная переменная:").pack(side=tk.LEFT, padx=5)
            
            self.cat_var_target = ttk.Combobox(self.params_frame, 
                                             values=list(df.select_dtypes(include=[object]).columns))
            self.cat_var_target.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            self.cat_var_target.current(0)
            
        elif plot_type == "Зависимость между двумя числовыми фичами":
            ttk.Label(self.params_frame, text="Ось X:").pack(side=tk.LEFT, padx=5)
            
            self.x_var = ttk.Combobox(self.params_frame, 
                                     values=list(df.select_dtypes(include=np.number).columns))
            self.x_var.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            self.x_var.current(0)
            
            ttk.Label(self.params_frame, text="Ось Y:").pack(side=tk.LEFT, padx=5)
            
            self.y_var = ttk.Combobox(self.params_frame, 
                                     values=list(df.select_dtypes(include=np.number).columns))
            self.y_var.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
            self.y_var.current(1)
        
        ttk.Button(self.params_frame, text="Построить график", command=self.generate_plot).pack(
            side=tk.RIGHT, padx=5)
        
        
    # Настройка вкладки моделей
    def setup_models(self):
        main_frame = ttk.Frame(self.models_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        model_frame = ttk.LabelFrame(main_frame, text="Выбор модели")
        model_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(model_frame, text="Модель:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.model_type = ttk.Combobox(model_frame, values=[
            'Naive Bayes',
            'KNN',
            'SVM',
            'Logistic Regression',
            'Decision Tree',
            'Random Forest',
            'Gradient Boosting',
        ])
        self.model_type.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.model_type.current(0)
        
        # Параметры клиента
        params_frame = ttk.LabelFrame(main_frame, text="Параметры клиента")
        params_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Возраст
        ttk.Label(params_frame, text="Возраст:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.person_age = ttk.Entry(params_frame)
        self.person_age.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Пол
        ttk.Label(params_frame, text="Пол:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.person_gender = ttk.Combobox(params_frame, values=['male', 'female'])
        self.person_gender.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.person_gender.current(0)
        
        # Образование
        ttk.Label(params_frame, text="Образование:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.person_education = ttk.Combobox(params_frame, 
                                           values=['Doctorate', 'Master', 'Bachelor', 'Associate', 'High School'])
        self.person_education.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.person_education.current(0)
        
        # Доход
        ttk.Label(params_frame, text="Годовой доход ($):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.person_income = ttk.Entry(params_frame)
        self.person_income.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        # Опыт работы
        ttk.Label(params_frame, text="Опыт работы (лет):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.person_emp_exp = ttk.Entry(params_frame)
        self.person_emp_exp.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        
        # Статус жилья
        ttk.Label(params_frame, text="Статус жилья:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.person_home_ownership = ttk.Combobox(params_frame, 
                                                values=['RENT', 'OTHER', 'MORTGAGE', 'OWN'])
        self.person_home_ownership.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.person_home_ownership.current(0)
        
        # Параметры кредита
        loan_frame = ttk.LabelFrame(main_frame, text="Параметры кредита")
        loan_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Сумма кредита
        ttk.Label(loan_frame, text="Сумма кредита ($):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.loan_amnt = ttk.Entry(loan_frame)
        self.loan_amnt.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Цель кредита
        ttk.Label(loan_frame, text="Цель кредита:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.loan_intent = ttk.Combobox(loan_frame, 
                                      values=['MEDICAL', 'EDUCATION', 'DEBTCONSOLIDATION', 'HOMEIMPROVEMENT', 'VENTURE', 'PERSONAL'])
        self.loan_intent.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.loan_intent.current(0)
        
        # Процентная ставка
        ttk.Label(loan_frame, text="Процентная ставка (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.loan_int_rate = ttk.Entry(loan_frame)
        self.loan_int_rate.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # Процент от дохода
        ttk.Label(loan_frame, text="Процент от дохода (%):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.loan_percent_income = ttk.Entry(loan_frame)
        self.loan_percent_income.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        # Кредитная история
        credit_frame = ttk.LabelFrame(main_frame, text="Кредитная история")
        credit_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Длина кредитной истории
        ttk.Label(credit_frame, text="Длина кредитной истории (лет):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cb_person_cred_hist_length = ttk.Entry(credit_frame)
        self.cb_person_cred_hist_length.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Кредитный рейтинг
        ttk.Label(credit_frame, text="Кредитный рейтинг:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.credit_score = ttk.Entry(credit_frame)
        self.credit_score.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Предыдущие дефолты
        ttk.Label(credit_frame, text="Предыдущие дефолты:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.previous_loan_defaults_on_file = ttk.Combobox(credit_frame, values=['No', 'Yes'])
        self.previous_loan_defaults_on_file.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.previous_loan_defaults_on_file.current(1)
        
        # Кнопка предсказания
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Выполнить предсказание", command=self.run_prediction).pack(
            side=tk.LEFT, padx=5)
        
        self.model_result_frame = ttk.LabelFrame(main_frame, text="Результаты предсказания")
        self.model_result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.model_result_text = tk.Text(self.model_result_frame, wrap=tk.WORD, height=5)
        self.model_result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def run_prediction(self):
        try:
            input_data = {
                'person_age': float(self.person_age.get()),
                'person_gender': self.person_gender.get(),
                'person_education': self.person_education.get(),
                'person_income': float(self.person_income.get()),
                'person_emp_exp': int(self.person_emp_exp.get()),
                'person_home_ownership': self.person_home_ownership.get(),
                'loan_amnt': float(self.loan_amnt.get()),
                'loan_intent': self.loan_intent.get(),
                'loan_int_rate': float(self.loan_int_rate.get()),
                'loan_percent_income': float(self.loan_percent_income.get()),
                'cb_person_cred_hist_length': float(self.cb_person_cred_hist_length.get()),
                'credit_score': int(self.credit_score.get()),
                'previous_loan_defaults_on_file': self.previous_loan_defaults_on_file.get()
            }
            
            model_name = self.model_type.get()
            prediction = self.models.predict(input_data, model_name)
            
            self.model_result_text.delete(1.0, tk.END)
            self.model_result_text.insert(tk.END, str(prediction))
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {str(e)}")
        
        
    # Отчеты
    def run_report1(self):
        try:
            report = clients_by_income_and_age(
                df,
                float(self.income_min.get()),
                float(self.income_max.get()),
                int(self.age_max.get()),
                self.rep1.get()
            )
            self.display_report(report)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {str(e)}")

    def run_report2(self):
        try:
            report = loan_intents_by_education(
                df,
                self.edu_combo.get(),
                self.rep2.get()
            )
            self.display_report(report)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка выполнения: {str(e)}")

    def run_report3(self):
        try:
            report = loans_by_interest_range(
                df,
                float(self.rate_min.get()),
                float(self.rate_max.get()),
                self.rep3.get()
            )
            self.display_report(report)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {str(e)}")

    def run_report4(self):
        try:
            report = pivot_avg_loan(df)
            self.display_report(report)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка выполнения: {str(e)}")

    def display_report(self, report):
        self.result_text.delete(1.0, tk.END)
        
        if isinstance(report, str):
            self.result_text.insert(tk.END, f"Отчет:\n {report}")
        elif isinstance(report, pd.DataFrame):
            if report.empty:
                self.result_text.insert(tk.END, "Нет подходящих записей.")
            else:
                self.result_text.insert(tk.END, report.to_markdown())
        else:
            self.result_text.insert(tk.END, "Неизвестный формат отчета")

    def generate_plot(self):        
        plot_type = self.plot_type.get()
        
        try:
            if plot_type == "Распределение категориальных фичей":
                plot_bar_count(df, self.cat_var.get())
                
            elif plot_type == "Распределение числовых фичей":
                plot_histogram(df, self.num_var1.get())
                
            elif plot_type == "Распределение числовых фичей по таргету":
                plot_kde(df, self.num_var1.get())
                
            elif plot_type == "Boxplot по таргету":
                plot_boxplot(df, self.num_var2.get(), self.show_outliers.get())
                
            elif plot_type == "Распределение категориальных фичей по TARGET":
                plot_count_by_target(df, self.cat_var_target.get())
                
            elif plot_type == "Зависимость между двумя числовыми фичами":
                plot_scatter(df, self.x_var.get(), self.y_var.get())
                
            elif plot_type == "Тепловая карта корреляций":
                plot_corr_heatmap(df)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка построения графика: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()