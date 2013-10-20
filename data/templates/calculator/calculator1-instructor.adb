with Ada.Text_IO;
with Ada.Integer_Text_IO;

use Ada.Text_IO;
use Ada.Integer_Text_IO;

procedure calculator1 is

First, Second, Result : integer;
Operator : character;
Valid : boolean;

begin

    loop
        Valid := true;

        Put("What do you want me to calculate? ");
        Get(First);
        Get(Operator);
        Get(Second);

        if Operator = '+' then
            Result := First + Second;
        elsif Operator = '-' then
            Result := First - Second;
        elsif Operator = '*' or Operator = 'x' then
            Result := First * Second;
        elsif Operator = '/' then
            Result := First / Second;
        elsif Operator = 'q' then
            -- Quit loop
            exit;
        else
            Put("Invalid operator: ");
            Put(Operator);
            Valid := false;
        end if;

        if Valid = true then
            Put(First, Width=>1);
            Put(" ");
            Put(Operator);
            Put(" ");
            Put(Second, Width=>1);
            Put(" = ");
            Put(Result, Width=>1);
            New_Line;
        end if;
    end loop;

end calculator1;
