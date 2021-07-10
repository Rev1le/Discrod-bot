type
   PElement = ^TypeElement;
   TypeElement = record
     number: integer;
     Data: string;
     Next: PElement;
    end;

var 
   pHead, pCur, pNew, pPred: PElement;
   j:integer; jup:string;
//------------------------просмотр
procedure smotri();
begin
  if pHead <> nil then
    begin
    pCur:=pHead;
    while pCur <> nil do
      begin
      writeln('на смотри: ',pCur^.Data);
      pCur:=pCur^.Next;
      end;
    end;  
end;
//------------------------вствака
procedure vstavka(plus: string);
begin
New(pNew);
pNew^.Data := plus;
if pHead <> nil then
//-----список не пустой
   begin
     if plus < pHead^.Data then
       begin
       pNew^.Next:=pHead;
       pHead:=pNew;
       end
     else
      begin
        pCur:=pHead;
        while pCur^.Next <> nil do
          begin
          if pCur^.Data > plus then
          begin
            pPred^.Next:=pNew;
            pNew^.Next:=pCur;
            exit;
          end;
          pCur:= pCur^.Next;
          end;
          pCur^.Next:=pNew;
          pNew^.Next:=nil;
        end;

   end
else
  begin
   pNew^.Next := nil;
   pHead := pNew;
   pCur := pNew;
  end;  
end;
//--------------------------поиск
procedure poisk();
begin

end;
//-------------------------удаление
procedure delete();
begin

end;
//---------------------------выход
procedure yxod();
begin

end;


begin

//---------------------меню действий
while true do
begin
writeln('выберете команду');
writeln('1-просмотр списка');
writeln('2-вставить элемент');
writeln('3-поиск элемента по фамилии');
writeln('4-удалить элемент');
writeln('5-выход');
Write('Ваша комада: ');
readln(j);
writeln;
case j of
  1: smotri;
  2:  
     begin
       write('Введите фамилию:  ');
       readln(jup);
       vstavka(jup); //вставка элемента
     end;
  3: poisk;
  4: delete;
  5: yxod;
end;
end;
end.