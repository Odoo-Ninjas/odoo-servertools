#1 mousetrap

NICHT MEHR VERWENDEN - DATAPOLICE VERWENDEN

wollte bei xzy kurz zync installieren um einen trigger zu konfigurieren; da gibts eine doofe konstellation bei liefersheinen; problem ist aber: der zync hat halt transaktionen und die muessen so stehen; d.h. ich kann nicht ohne the fly einen constraint pruefen, weil in der transaktion bei create der lieferschein nicht da ist.

ich mache ein mousetrap modul: da kann man dann sagen: bei create von lieferschein und oder stock move mach folgende pruefeung: ...code...

der stacktrace wird dann protokolliert abgespeichert; d.h. man ist nicht auf den user angewiesen, dass die den stacktrace richtig rauskopieren.

#2 Contributors

* Marc Wimmer <marc@itewimmer.de>

