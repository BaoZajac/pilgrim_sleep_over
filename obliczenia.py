from uczestnicy import Pielgrzymi
from noclegi import Noclegi
from uczestnicy import pielg
from noclegi import noclegi    # TODO: importujemy obiekt czy klasę? (noclegi czy Noclegi?)


class PrzydzielNocleg():
    def __init__(self, data):
        self.data = data
        self.przydzielone_noclegi = {}
        if self.data not in self.przydzielone_noclegi.keys():
            self.przydzielone_noclegi[self.data] = []

        self.nocl_dom, self.nocl_il = noclegi.suma_nocl_data(data)
        # print(f"Suma noclegów: {self.nocl_il}")
        self.wszyscy_pielgrzymi = pielg.podsum_il_wg_plci()
        # print(f"Suma pielgrzymów: {self.wszyscy_pielgrzymi[1]}")

        self.zestaw_prioryt = pielg.podsum_il_wg_prioryt()
        # print(f"Zestawienie priorytetów: {self.zestaw_prioryt}")
        # # print(sorted(b.items()))
        # print(f"Il osób z priorytetem z grupy A: {self.zestaw_prioryt[0]}")

        self.nocl_il = 5
        # print(self.przydzielone_noclegi)
        # print("----------")


    def noclegi_dla_pielgrzymow(self):
        if self.nocl_il < self.zestaw_prioryt[0]:
            a = "Problem z noclegami dla funkcyjnych priorytetowych! Zgłoś zaistniałą sytuację liderowi kwatermistrzów"
            # print(a)
            return a

        elif self.zestaw_prioryt[0] + self.zestaw_prioryt[1] + self.zestaw_prioryt[2] > self.nocl_il \
                >= self.zestaw_prioryt[0]:
            # print("Wszyscy z grupy A i część z grupy B")
            # print("Przydziel nocleg wszystkim z grupy A, reszta do grupy B wg priorytetu")
            self.przydzielone_noclegi[self.data] = self.przydziel_maly_dom()

        else:
            print("tu")
        print(11, self.przydzielone_noclegi)

    def przydziel_maly_dom(self):
        # print(12, noclegi.zestawienie_malych_domow(self.data))
        # print(4, noclegi.zestawienie_malych_domow(self.data).keys())
        return noclegi.zestawienie_malych_domow(self.data)


# def zapisz_noclegi(self):
    #     ...

przydziel_nocleg = PrzydzielNocleg("2022-08-03")
przydziel_nocleg.noclegi_dla_pielgrzymow()
# przydziel_nocleg.przydziel_maly_dom()

