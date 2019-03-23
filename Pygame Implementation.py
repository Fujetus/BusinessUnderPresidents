import pygame as pg
import requests

def main():
    presidents = "ford carter reagan bush clinton obama"
    out_thing = []
    year = [["FORD", "1976", "1977"], ["CARTER", "1977", "1981"], ["REAGAN", "1981", "1989"], ["BUSH1", "1989", "1993"],["CLINTON", "1993", "2001"], ["BUSH2", "2001", "2009"]]
    screen = pg.display.set_mode((640, 480))
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    input_box = pg.Rect(220, 210, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    name = ''
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        name: str = name.upper()
                        for num in range(6):
                            temp = []
                            temp = year[num]
                            if temp[0] == name:
                                out_thing.append(temp[0])
                                out_thing.append(temp[1])
                                out_thing.append(temp[2])
                        # print(out_thing)
                        startyear = out_thing[1]
                        endyear = out_thing[2]
                        jobsum = 0
                        for year in range(int(startyear), int(endyear)):
                            url = "https://api.census.gov/data/timeseries/bds/firms?get=estabs_entry_rate,estabs_exit_rate,estabs_entry,net_job_creation,ifsize&for=us:*&year2=" + str(
                                year) + "&key=b2fe9fbe9c805f2fb54e8c0398c97450a3132cde"
                            page = requests.get(url)
                            result = page.json()
                            for x in range(1, len(result)):
                                jobsum += int(result[x][3])

                        ni = ("The net sum of job creation in " + str(
                            name.capitalize()) + "'s complete administration is " + str(jobsum))
                        gg = ("This indicates that per year an average of number of " + str(
                            int((int(jobsum) / (int(endyear) - int(startyear))))) + " jobs were created")

                        net_poverty = 0
                        url_poverty_endyear = 'https://api.census.gov/data/timeseries/poverty/histpov2?get=PCTPOV&for=us:*&time=' + str(
                            endyear) + '&RACE=1' + "&key=b2fe9fbe9c805f2fb54e8c0398c97450a3132cde"
                        url_poverty_startyear = 'https://api.census.gov/data/timeseries/poverty/histpov2?get=PCTPOV&for=us:*&time=' + str(
                            startyear) + '&RACE=1' + "&key=b2fe9fbe9c805f2fb54e8c0398c97450a3132cde"

                        page = requests.get(url_poverty_endyear)
                        api_data_poverty_endyear = page.json()
                        page = requests.get(url_poverty_startyear)
                        api_data_poverty_startyear = page.json()
                        net_poverty = float(api_data_poverty_endyear[1][0]) - float(api_data_poverty_startyear[1][0])
                        increase_or_decrease = ""
                        if net_poverty < 0:
                            increase_or_decrease = "decrease"
                        else:
                            increase_or_decrease = "increase"
                        er = ("When " + name.upper() + " was president, the country experienced a ",
                              abs(round(net_poverty, 1)), "% " + increase_or_decrease + " in poverty rate")
                        name = ''
                    elif event.key == pg.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

        screen.fill((30, 30, 30))
        # Render the current name.
        txt_surface = font.render(name, True, color)
        # Resize the box if the name is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the name.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()