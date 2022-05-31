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

    def przydziel_jakikolwiek_nocleg_komukolwiek_w_danym_dniu(self):
        noclegi_wynikowe = {}
        noclegi_w_dniu = noclegi.lista_nocleg_data(self.data)
        for nocleg in noclegi_w_dniu:
            il_nocl = nocleg[7]
            noclegi_wynikowe[tuple(nocleg)] = []
            n = 0
            while il_nocl > 0:
                noclegi_wynikowe[tuple(nocleg)].append(pielg.wszyscy_pielgrzymi[n])
                il_nocl -= 1
                n += 1
        print(2, noclegi_wynikowe)

    def noclegi_dla_pielgrzymow(self):
        # brakuje noclegów nawet dla funkcyjni_0
        if self.nocl_il < self.zestaw_prioryt[0]:
            a = "Problem z noclegami dla funkcyjnych priorytetowych! Zgłoś zaistniałą sytuację liderowi kwatermistrzów"
            # print(a)
            return a
        # noclegi są dla funkcyjni_0 i części funkcyjni_1
        elif self.zestaw_prioryt[0] + self.zestaw_prioryt[1] + self.zestaw_prioryt[2] > self.nocl_il \
                >= self.zestaw_prioryt[0]:
            # print("Wszyscy z grupy A i część z grupy B")
            # print("Przydziel nocleg wszystkim z grupy A, reszta do grupy B wg priorytetu")
            self.przydzielone_noclegi[self.data] = self.przydziel_maly_dom()
            il_nocl_w_malych_domach = self.przydziel_maly_dom()[1]
            # print(1, il_nocl_w_malych_domach)
            # for el in noclegi.zestawienie_malych_domow(self.data)[1]:
            #     noclegi.zestawienie_malych_domow(self.data)[1][el][7]
            # if il_nocl_w_malych_domach < self.zestaw_prioryt[0]:
            #     ... # TODO: przyporządkuj jakikolwiek dom
            # for el in
        else:
            print("tu")
        # print(1, self.przydzielone_noclegi)

    def przydziel_maly_dom(self):
        # print(12, noclegi.zestawienie_malych_domow(self.data))
        # print(4, noclegi.zestawienie_malych_domow(self.data).keys())
        return noclegi.zestawienie_malych_domow(self.data)



# def zapisz_noclegi(self):
    #     ...

przydziel_nocleg = PrzydzielNocleg("2022-08-03")
przydziel_nocleg.noclegi_dla_pielgrzymow()
# przydziel_nocleg.przydziel_maly_dom()
# print("f0:", pielg.funkcyjni_0)
przydziel_nocleg.przydziel_jakikolwiek_nocleg_komukolwiek_w_danym_dniu()

# noclegi.lista_nocleg_data("2022-08-03")
