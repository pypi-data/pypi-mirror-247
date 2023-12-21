from ... import exceptions


class Disconnect:
    async def disconnect(self):
        try:
            await self.connection.close()
            #self._logger.info(f'the client was disconnected')

        except AttributeError:
            raise exceptions.NoConnection(
                'You must first connect the Client'
                ' with the *.connect() method')