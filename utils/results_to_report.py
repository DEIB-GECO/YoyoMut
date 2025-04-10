import os
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from PIL import Image
import fpdf
from matplotlib.ticker import MultipleLocator
from datetime import datetime


def generate_plot(name, df):
    """Reads a CSV file and generates a line plot, saving it as an image."""
    # plt.figure(figsize=(6, 4))
    # plt.plot(df.index, df.iloc[:, 1], marker='o', linestyle='-')  # Plot 2nd column
    # plt.title(f"Line Plot for {os.path.basename(csv_path)}")
    # plt.xlabel("Index")
    # plt.ylabel("Value")
    #
    # plot_path = csv_path.replace(".csv", ".png")
    # plt.savefig(plot_path, bbox_inches='tight')

    fig, ax = plt.subplots()
    x = df['start-date']
    ax.plot(x, df['avg-proportion'], label='Proportion')
    ax.fill_between(
        x, df['ci-lower-avg'], df['ci-upper-avg'], color='b', alpha=.15, label='Confidence interval')
    ax.set_ylim(ymin=0, ymax=1.1)
    ax.xaxis.set_major_locator(MultipleLocator(20))
    ax.set_title('Proportion through time')
    fig.autofmt_xdate(rotation=45)

    ax.legend()

    plot_path = './graphs/' + name.replace('.csv', '.png').replace(':', '_')
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()
    return plot_path


def get_name(file_name):
    if 'ins_S' in file_name:
        params = file_name[6:-4].replace('_', ':')
        name = 'ins_S:' + params
    else:
        params = file_name[2:-4].replace('_', ':')
        name = 'S:' + params
    return name


def results_to_PDF(report_path, report_title, report_name, data_dict, parameters):
    # for each mutation/insertion:
    # 1. name
    # 2. total sequences
    # 3. list of hills with max proportion, start date, end date, length
    # one mutation per page
    # report file is saved as path+name given as arguments
    # would also add the date when the report was generated (in the name of the file as well as on the first page)

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 100, txt=report_title, ln=True, align="C")
    intro = "In this report the parameters used were: "
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 0, txt=intro, ln=True)
    parameter_bullet_points = []
    for param in parameters:
        parameter_bullet_points.append(f"- {param}: {parameters[param]}")

    y_position = 120
    for point in parameter_bullet_points:
        pdf.set_xy(20, y_position)
        pdf.cell(0, 10, point, ln=True)
        y_position += 10

    file_names = list(data_dict.keys())
    file_names.sort()

    for file in file_names:
        # if not os.path.exists(data_path + file):  # Skip missing files
        #     print('The file ', file, ' doesn\'t exist.\n')
        #     continue

        pdf.add_page()

        # Add file name as title
        pdf.set_font("Helvetica", "B", 16)
        name = get_name(file)
        pdf.cell(0, 20, txt=name, ln=True, align="C")

        # Generate bullet points
        hills_df = data_dict[file]['hills']
        df = data_dict[file]['data']
        hill_count = hills_df.shape[0]
        total_sequences = int((df['avg-proportion'] * df['total-count']).sum())
        bullet_points = [
            f"- Number of hills: {hill_count}",
            f"- Total sequences: {total_sequences}"
        ]

        pdf.set_font("Helvetica", size=12)
        y_position = 40
        for point in bullet_points:
            pdf.set_xy(20, y_position)
            pdf.cell(0, 10, point, ln=True)
            y_position += 10

        for i in range(hill_count):
            if i % 2 == 0:
                x_position = 20
            else:
                x_position = 100
            pdf.set_xy(x_position, y_position)
            pdf.cell(0, 20, f"{i + 1}:", ln=True)
            pdf.set_xy(x_position+5, y_position)
            pdf.cell(10, 20, f" Start date: {hills_df.iloc[i]['start-date']}", ln=True)
            pdf.set_xy(x_position+5, y_position + 10)
            pdf.cell(10, 20, f" End date: {hills_df.iloc[i]['end-date']}", ln=True)
            pdf.set_xy(x_position+5, y_position + 20)
            length_days = hills_df.iloc[i]['length-days']
            if pd.isna(length_days):
                date_format = '%Y-%m-%d'
                last_day = df.iloc[-1]['end-date']
                length_days = datetime.strptime(last_day, date_format) - datetime.strptime(hills_df.iloc[i]['start-date'], date_format)
                days_string = str(length_days.days) + ' days for now'
            else:
                days_string = str(int(length_days)) + ' days'
            pdf.cell(10, 20, f" Length: {days_string}", ln=True)
            if i % 2 == 1:
                y_position += 30
            elif i % 2 == 0 and i == hill_count - 1:
                y_position += 30

        # Generate and insert plot
        plot_path = generate_plot(file, df)
        if os.path.exists(plot_path):
            pdf.image(plot_path, x=30, y=y_position + 10, w=150)

    # Save final PDF
    name = f"Report_{report_name}"
    date = datetime.today().strftime("%Y-%m-%d")
    report_file = f"{report_path}{name}_{date}.pdf"
    counter = 1
    while os.path.exists(report_file):
        report_file = f"{report_path}{name}_{date}_({counter}).pdf"
        counter += 1
    pdf.output(report_file)
    print("PDF generated successfully!")
